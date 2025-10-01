
"""
浏览器驱动管理模块（已修复：自动匹配 Chrome/Chromedriver 主版本，失败后用 version_main 重试；不依赖 uc.install）

- 首次用 undetected_chromedriver 正常启动
- 若遇到 "session not created" 且报 Chrome 主版本不匹配：解析当前浏览器主版本，使用 uc.Chrome(version_main=<当前主版本>) 重试
- 兼容 CI：附加稳定参数，可用 CHROME_BINARY / GOOGLE_CHROME_SHIM 指定 Chrome 可执行文件
- SafeChrome 包装避免析构/句柄异常
"""

import logging
import os
import re
from typing import Optional, Dict, Any

# 优先使用 undetected_chromedriver
try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import (
        TimeoutException,
        NoSuchElementException,
        WebDriverException,
    )

    # 修复 uc.__del__
    def safe_del(self):
        try:
            if hasattr(self, "_is_patched") and self._is_patched:
                return
        except Exception:
            pass
    if hasattr(uc.Chrome, "__del__"):
        uc.Chrome.__del__ = safe_del

    UNDETECTED_AVAILABLE = True
except ImportError:
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import (
            TimeoutException,
            NoSuchElementException,
            WebDriverException,
        )
        UNDETECTED_AVAILABLE = False
    except ImportError:
        raise ImportError("请安装 selenium：pip install selenium")


class SafeChrome:
    """安全 Chrome 驱动包装器，防止析构时异常"""

    def __init__(self, driver):
        self._driver = driver
        self._is_closed = False

    def __getattr__(self, name):
        if self._is_closed:
            raise RuntimeError("Driver has been closed")
        return getattr(self._driver, name)

    def close(self):
        if not self._is_closed and self._driver:
            try:
                self._driver.close()
            except Exception:
                pass

    def quit(self):
        if not self._is_closed and self._driver:
            try:
                try:
                    self._driver._is_patched = True
                except Exception:
                    pass
                self._driver.quit()
            except Exception:
                pass
            finally:
                self._is_closed = True
                self._driver = None

    def __del__(self):
        # 避免在垃圾回收时出现句柄错误
        pass


class BrowserDriverManager:
    """浏览器驱动管理器（支持自动版本匹配与重试）"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.driver: Optional[SafeChrome] = None
        self._is_cleanup_done = False
        self.wait: Optional[WebDriverWait] = None

    def _build_options(self, headless: bool):
        """构建 Chrome 选项（兼容 uc 与 selenium）"""
        if UNDETECTED_AVAILABLE:
            options = uc.ChromeOptions()
        else:
            options = Options()

        # Headless：新版 Chrome 建议 --headless=new
        if headless:
            try:
                options.add_argument("--headless=new")
            except Exception:
                options.add_argument("--headless")
            self.logger.debug("启用无头模式")
        else:
            self.logger.debug("使用有头模式（显示浏览器窗口）")

        # 通用参数
        browser_args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "--disable-popup-blocking",
        ]

        # CI 环境参数
        if os.getenv("GITHUB_ACTIONS") or os.getenv("CI"):
            self.logger.debug("检测到 CI 环境，添加额外配置")
            ci_args = [
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-features=TranslateUI",
                "--disable-ipc-flooding-protection",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-default-apps",
                "--disable-extensions",
                "--disable-plugins",
                "--disable-sync",
                "--disable-translate",
                "--hide-scrollbars",
                "--mute-audio",
                "--no-zygote",
                "--disable-background-networking",
                "--disable-web-security",
                "--allow-running-insecure-content",
                "--window-size=1920,1080",
                "--font-render-hinting=none",
                "--disable-font-subpixel-positioning",
                "--force-device-scale-factor=1",
            ]
            browser_args.extend(ci_args)

        for arg in browser_args:
            try:
                options.add_argument(arg)
                self.logger.debug(f"添加浏览器参数: {arg}")
            except Exception:
                pass

        # 浏览器偏好
        prefs = {
            "profile.default_content_setting_values": {"popups": 1},
            "webkit.webprefs.fonts.standard.Hans": "SimSun",
            "webkit.webprefs.fonts.serif.Hans": "SimSun",
            "webkit.webprefs.fonts.sansserif.Hans": "SimHei",
            "webkit.webprefs.fonts.cursive.Hans": "SimSun",
            "webkit.webprefs.fonts.fantasy.Hans": "SimSun",
            "webkit.webprefs.fonts.pictograph.Hans": "SimSun",
            "webkit.webprefs.default_encoding": "UTF-8",
        }
        if os.getenv("GITHUB_ACTIONS") or os.getenv("CI"):
            prefs.update({
                "webkit.webprefs.fonts.standard.Hans": "Noto Sans CJK SC",
                "webkit.webprefs.fonts.serif.Hans": "Noto Serif CJK SC",
                "webkit.webprefs.fonts.sansserif.Hans": "Noto Sans CJK SC",
                "webkit.webprefs.fonts.cursive.Hans": "Noto Sans CJK SC",
                "webkit.webprefs.fonts.fantasy.Hans": "Noto Sans CJK SC",
                "webkit.webprefs.fonts.pictograph.Hans": "Noto Sans CJK SC",
            })
            self.logger.debug("配置 CI 环境中文字体偏好")
        try:
            # uc 与 selenium 的 options 都支持 add_experimental_option
            options.add_experimental_option("prefs", prefs)
            self.logger.debug("配置浏览器偏好设置: 弹出窗口允许、中文字体支持")
        except Exception:
            pass

        # 指定 Chrome 二进制（CI/容器常用）
        binary = os.getenv("CHROME_BINARY") or os.getenv("GOOGLE_CHROME_SHIM")
        if binary:
            try:
                options.binary_location = binary
                self.logger.debug(f"使用指定 Chrome 二进制: {binary}")
            except Exception:
                self.logger.debug("设置 binary_location 失败，忽略")

        return options

    def _init_driver_uc(self, options):
        """
        优先用 undetected_chromedriver 初始化；若版本不匹配，解析当前 Chrome 主版本并用 version_main 重试。
        不依赖 uc.install（兼容老版本 uc）。
        """
        try:
            return uc.Chrome(options=options)
        except Exception as e:
            msg = str(e)
            # 典型报错：supports Chrome version XXX ... Current browser version is YYY
            m = re.search(
                r"supports Chrome version\s*(\d+).*?Current browser version is\s*(\d+)",
                msg,
                flags=re.IGNORECASE | re.DOTALL,
            )
            m_current = re.search(r"Current browser version is\s*(\d+)", msg, flags=re.IGNORECASE)
            curr_major = None
            if m and m.group(2):
                curr_major = int(m.group(2))
            elif m_current and m_current.group(1):
                curr_major = int(m_current.group(1))

            if curr_major:
                self.logger.warning(
                    f"检测到 Chrome/Chromedriver 主版本不匹配，按当前浏览器 {curr_major} 版本重试（version_main）……"
                )
                try:
                    # 绝大多数 uc 版本都支持 version_main
                    return uc.Chrome(options=options, version_main=curr_major)
                except TypeError:
                    # 极老版本 uc 可能不支持 version_main：最后一次直接重试（让底层自行解析）
                    self.logger.warning("当前 undetected_chromedriver 不支持 version_main，回退到默认启动重试……")
                    return uc.Chrome(options=options)
            # 未能提取到主版本，抛出原异常
            raise

    def create_driver(self, config: Dict[str, Any]) -> bool:
        """创建浏览器驱动（自动匹配版本）"""
        try:
            self.logger.info("开始创建浏览器驱动")
            headless = bool(config.get("headless", True))
            options = self._build_options(headless=headless)

            self.logger.debug("开始初始化浏览器实例")
            if UNDETECTED_AVAILABLE:
                raw_driver = self._init_driver_uc(options)
            else:
                # 标准 selenium：交给 Selenium Manager 解决驱动（需新版本 selenium）
                raw_driver = webdriver.Chrome(options=options)  # type: ignore[name-defined]

            self.driver = SafeChrome(raw_driver)
            self.wait = WebDriverWait(self.driver, int(config.get("wait_timeout", 10)))

            # 打印版本信息
            try:
                caps = getattr(self.driver, "capabilities", {}) or {}
                browser_version = caps.get("browserVersion") or caps.get("version") or "Unknown"
                chrome_info = caps.get("chrome") or {}
                driver_version = chrome_info.get("chromedriverVersion") or "Unknown"
                self.logger.debug(f"浏览器版本: {browser_version}")
                self.logger.debug(f"驱动版本: {driver_version}")
            except Exception as e:
                self.logger.debug(f"获取浏览器信息失败: {e}")

            self.logger.info("浏览器驱动创建成功")
            return True

        except Exception as e:
            self.logger.error(f"创建浏览器驱动失败: {e}")
            return False

    def get_driver(self):
        return self.driver

    def get_wait(self) -> Optional[WebDriverWait]:
        return self.wait

    def quit_driver(self) -> None:
        """关闭浏览器驱动"""
        if self.driver and not self._is_cleanup_done:
            try:
                try:
                    self.driver.close()
                except Exception:
                    pass
                self.driver.quit()
                self.logger.info("浏览器已关闭")
            except Exception as e:
                self.logger.warning(f"关闭浏览器失败: {e}")
            finally:
                self._is_cleanup_done = True
                self.driver = None
                self.wait = None

    def force_quit_driver(self) -> None:
        """强制关闭浏览器驱动（用于异常情况）"""
        if self.driver and not self._is_cleanup_done:
            try:
                # 终止 chromedriver 进程（若可用）
                try:
                    if hasattr(self.driver, "_driver") and hasattr(self.driver._driver, "service"):
                        service = self.driver._driver.service
                        if hasattr(service, "process"):
                            process = service.process
                            if process and getattr(process, "poll", lambda: None)() is None:
                                process.terminate()
                                try:
                                    process.wait(timeout=3)
                                except Exception:
                                    pass
                except Exception:
                    pass
                # 正常退出
                self.driver.quit()
                self.logger.info("浏览器已强制关闭")
            except Exception as e:
                self.logger.warning(f"强制关闭浏览器失败: {e}")
            finally:
                self._is_cleanup_done = True
                self.driver = None
                self.wait = None

    def is_driver_alive(self) -> bool:
        if not self.driver:
            return False
        try:
            _ = self.driver.current_url
            return True
        except Exception:
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    mgr = BrowserDriverManager()
    ok = mgr.create_driver({"headless": True})
    print("create_driver:", ok)
    mgr.quit_driver()
