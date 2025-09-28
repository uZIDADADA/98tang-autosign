#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
98tang-autosign - 主入口文件

98堂论坛自动签到系统，专门为98堂论坛优化的自动签到工具。

特性:
- 智能浏览器自动化
- 拟人化操作行为
- 灵活的配置管理
- 详细的日志记录
- 模块化架构设计

使用方法:
    python main.py [--debug]

参数:
    --debug: 启用调试模式，输出详细日志信息
"""

import sys
import os
import argparse
import signal
import atexit
from pathlib import Path

# 在 0 ~ 7200 秒之间随机延时（2 小时 = 7200 秒）
delay = random.randint(0, 3600)
print(f"随机延时 {delay // 60} 分钟后开始执行签到任务...")
time.sleep(delay)

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.app import AutoSignApp

# 全局变量用于存储应用实例
_app_instance = None


def cleanup_handler():
    """清理处理器"""
    global _app_instance
    if _app_instance:
        try:
            print("\n\ud83e\uddf9 正在清理资源...")
            _app_instance._cleanup()
            print("✅ 资源清理完成")
        except Exception as e:
            print(f"⚠️ 清理资源时出错: {e}")


def signal_handler(signum, frame):
    """信号处理器"""
    print(f"\n\ud83d\udea8 接收到信号 {signum}，正在安全退出...")
    cleanup_handler()
    sys.exit(128 + signum)


# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
if hasattr(signal, "SIGTERM"):
    signal.signal(signal.SIGTERM, signal_handler)  # 终止信号

# 注册退出处理器
atexit.register(cleanup_handler)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="98tang-autosign - 98堂论坛自动签到系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py              # 正常模式运行
  python main.py --debug      # 调试模式运行

配置文件:
  本地运行：程序会自动读取 config.env 配置文件
  如果不存在，请复制 config.env.example 并修改配置
  
  CI环境：程序会自动使用环境变量，无需配置文件
        """,
    )

    parser.add_argument(
        "--debug", action="store_true", help="启用调试模式（输出详细日志信息）"
    )

    parser.add_argument(
        "--config", default="config.env", help="指定配置文件路径（默认: config.env）"
    )

    args = parser.parse_args()

    # 检查配置文件是否存在（仅在本地运行时检查）
    # GitHub Actions 等 CI 环境使用环境变量，无需配置文件
    config_path = Path(args.config)
    is_ci_environment = os.getenv("GITHUB_ACTIONS") or os.getenv("CI")

    if not config_path.exists() and not is_ci_environment:
        print(f"❌ 配置文件不存在: {args.config}")
        print("请复制 config.env.example 为 config.env 并填写配置")
        print("或者设置环境变量 SITE_USERNAME 和 SITE_PASSWORD")
        return 1

    print("=" * 50)
    print("🤖 98tang-autosign")
    print("=" * 50)

    if args.debug:
        print("🔍 运行在调试模式")

    try:
        # 在CI环境下默认启用DEBUG模式
        debug_mode = args.debug or is_ci_environment
        if is_ci_environment and not args.debug:
            print("🔍 检测到CI环境，自动启用DEBUG模式以获得详细日志")

        # 创建应用实例
        global _app_instance
        _app_instance = AutoSignApp(config_file=args.config, debug_mode=debug_mode)
        app = _app_instance

        # 运行应用
        success = app.run()

        if success:
            print("✅ 程序执行完成")
            # 清理全局引用
            _app_instance = None
            return 0
        else:
            print("❌ 程序执行失败")
            # 清理全局引用
            _app_instance = None
            return 1

    except KeyboardInterrupt:
        print("\n⚠️  程序被用户中断")
        # 清理全局引用
        _app_instance = None
        return 130

    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        if args.debug or is_ci_environment:
            import traceback

            print("详细错误信息:")
            traceback.print_exc()

        # 尝试发送错误通知（如果应用实例存在且有Telegram通知器）
        if (
            _app_instance
            and hasattr(_app_instance, "telegram_notifier")
            and _app_instance.telegram_notifier
        ):
            try:
                _app_instance.telegram_notifier.send_error(str(e), "程序启动异常")

                # 如果启用了日志推送且有日志文件，则发送日志文件
                if (
                    _app_instance.config_manager.get("TELEGRAM_SEND_LOG_FILE", False)
                    and hasattr(_app_instance, "logger_manager")
                    and _app_instance.logger_manager
                ):
                    current_log_file = (
                        _app_instance.logger_manager.get_current_log_file()
                    )
                    if current_log_file and os.path.exists(current_log_file):
                        try:
                            _app_instance.telegram_notifier.send_log_file(
                                current_log_file
                            )
                        except Exception:
                            pass  # 避免日志发送失败影响程序退出
            except Exception:
                pass  # 避免通知发送失败影响程序退出

        # 清理全局引用
        _app_instance = None
        return 1


if __name__ == "__main__":
    sys.exit(main())
