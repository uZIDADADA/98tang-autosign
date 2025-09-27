# 📋 配置参数详细说明

本文档详细介绍了 98tang-autosign 的所有配置参数，包括默认值、使用说明和注意事项。

## 📖 目录

- [🔑 必备配置](#-必备配置必填)
- [🔧 基础功能配置](#-基础功能配置)
- [📱 Telegram通知配置](#-telegram通知配置)
- [🤖 拟人化行为配置](#-拟人化行为配置可选提高真实性)
- [⚡ 高级配置](#-高级配置通常不需要修改)
- [🔄 配置优先级](#-配置优先级)
- [✅ 配置验证](#-配置验证)

---

## 🔑 必备配置（必填）

这些配置是程序运行的基本要求，必须正确填写。

### SITE_USERNAME
- **类型**: 字符串
- **默认值**: 无（必填）
- **说明**: 98tang论坛的用户名
- **示例**: `SITE_USERNAME=your_username`

### SITE_PASSWORD
- **类型**: 字符串
- **默认值**: 无（必填）
- **说明**: 98tang论坛的密码
- **示例**: `SITE_PASSWORD=your_password`
- **安全提示**: 密码在日志中会被自动掩码处理

---

## 🔧 基础功能配置

### BASE_URL
- **类型**: 字符串
- **默认值**: `https://www.sehuatang.org`
- **说明**: 论坛的基础网址，通常不需要修改
- **示例**: `BASE_URL=https://www.sehuatang.org`

### ENABLE_CHECKIN
- **类型**: 布尔值
- **默认值**: `true`
- **说明**: 是否启用签到功能
- **示例**: `ENABLE_CHECKIN=true`
- **可选值**: `true`、`false`

### ENABLE_SECURITY_QUESTION
- **类型**: 布尔值
- **默认值**: `false`
- **说明**: 是否启用安全提问处理（如果你的账号设置了安全提问，请设为true）
- **示例**: `ENABLE_SECURITY_QUESTION=false`
- **可选值**: `true`、`false`

### SECURITY_QUESTION
- **类型**: 字符串
- **默认值**: `您个人计算机的型号`
- **说明**: 你在网站设置的安全提问内容
- **示例**: `SECURITY_QUESTION=您个人计算机的型号`
- **注意**: 只有当 `ENABLE_SECURITY_QUESTION=true` 时才需要填写

### SECURITY_ANSWER
- **类型**: 字符串
- **默认值**: 无
- **说明**: 安全提问的答案
- **示例**: `SECURITY_ANSWER=your_answer`
- **注意**: 只有当 `ENABLE_SECURITY_QUESTION=true` 时才需要填写
- **安全提示**: 答案在日志中会被自动掩码处理

---

## 📱 Telegram通知配置

### ENABLE_TELEGRAM_NOTIFICATION
- **类型**: 布尔值
- **默认值**: `false`
- **说明**: 是否启用Telegram通知
- **示例**: `ENABLE_TELEGRAM_NOTIFICATION=false`
- **可选值**: `true`、`false`

### TELEGRAM_BOT_TOKEN
- **类型**: 字符串
- **默认值**: 无
- **说明**: Telegram机器人Token（找@BotFather申请）
- **示例**: `TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
- **注意**: 只有当 `ENABLE_TELEGRAM_NOTIFICATION=true` 时才需要填写
- **安全提示**: Token在日志中会被自动掩码处理

### TELEGRAM_CHAT_ID
- **类型**: 字符串
- **默认值**: 无
- **说明**: Telegram聊天ID（找@userinfobot获取你的用户ID）
- **示例**: `TELEGRAM_CHAT_ID=123456789`
- **注意**: 只有当 `ENABLE_TELEGRAM_NOTIFICATION=true` 时才需要填写
- **安全提示**: Chat ID在日志中会被自动掩码处理

### TELEGRAM_PROXY_URL
- **类型**: 字符串
- **默认值**: 无（可选）
- **说明**: Telegram代理URL（国内用户可能需要）
- **示例**: `TELEGRAM_PROXY_URL=http://127.0.0.1:1080`
- **注意**: 可选配置，国内网络环境可能需要
- **安全提示**: 代理URL在日志中会被自动掩码处理

### TELEGRAM_SEND_LOG_FILE
- **类型**: 布尔值
- **默认值**: `false`（代码中实际默认值）
- **说明**: 是否发送详细日志文件（便于调试）
- **示例**: `TELEGRAM_SEND_LOG_FILE=true`
- **可选值**: `true`、`false`
- **注意**: config.env.example中设为true，但代码默认为false

### TELEGRAM_SEND_SCREENSHOT
- **类型**: 布尔值
- **默认值**: `false`（代码中实际默认值）
- **说明**: 是否发送页面截图（便于了解执行状态）
- **示例**: `TELEGRAM_SEND_SCREENSHOT=true`
- **可选值**: `true`、`false`
- **注意**: config.env.example中设为true，但代码默认为false

---

## 🤖 拟人化行为配置（可选，提高真实性）

### ENABLE_REPLY
- **类型**: 布尔值
- **默认值**: `true`
- **说明**: 是否启用随机回复功能
- **示例**: `ENABLE_REPLY=true`
- **可选值**: `true`、`false`

### REPLY_COUNT
- **类型**: 整数
- **默认值**: `2`
- **说明**: 回复数量（建议1-3个）
- **示例**: `REPLY_COUNT=2`
- **建议范围**: 1-3

### ENABLE_RANDOM_BROWSING
- **类型**: 布尔值
- **默认值**: `true`
- **说明**: 是否启用随机浏览
- **示例**: `ENABLE_RANDOM_BROWSING=true`
- **可选值**: `true`、`false`

### BROWSE_PAGE_COUNT
- **类型**: 整数
- **默认值**: `3`
- **说明**: 随机浏览页面数量（建议2-5页）
- **示例**: `BROWSE_PAGE_COUNT=3`
- **建议范围**: 2-5

### REPLY_MESSAGES
- **类型**: 字符串（分号分隔）
- **默认值**: 内置默认消息列表
- **说明**: 回复消息模板（用分号;分隔多个消息）
- **示例**: `REPLY_MESSAGES=感谢分享资源，收藏了;好资源收藏了，谢谢楼主`
- **默认消息列表**:
  - 感谢分享资源，收藏了
  - 好资源收藏了，谢谢楼主
  - 感谢楼主的精彩分享
  - 谢谢分享，非常实用
  - 好内容，支持一下楼主

### COMMENT_INTERVAL
- **类型**: 整数
- **默认值**: `15`
- **说明**: 回复间隔时间（秒，不低于15秒，避免频繁操作）
- **示例**: `COMMENT_INTERVAL=15`
- **最小值**: 15秒（强制限制）

### WAIT_AFTER_LOGIN
- **类型**: 整数
- **默认值**: `5`
- **说明**: 登录后等待时间（秒，模拟人工操作）
- **示例**: `WAIT_AFTER_LOGIN=5`

### USE_DEEPSEEK
- **类型**: 布尔
- **默认值**: `false`
- **说明**: 是否通过DeepSeek AI生成回复内容（需要配置DEEPSEEK_API_KEY）
- **示例**: `### USE_DEEPSEEK=true`


### DEEPSEEK_API_KEY
- **类型**: 字符串
- **默认值**: `无`
- **说明**:  DeepSeek AI的API Key（前往https://www.deepseek.ai/注册获取）
- **示例**: `### DEEPSEEK_API_KEY=sk-****`

---

## ⚡ 高级配置（通常不需要修改）

### HEADLESS
- **类型**: 布尔值
- **默认值**: `true`
- **说明**: 是否无头模式运行（true=不显示浏览器窗口）
- **示例**: `HEADLESS=true`
- **可选值**: `true`、`false`
- **建议**: 调试时设为false，正式运行设为true

### LOG_LEVEL
- **类型**: 字符串
- **默认值**: `DEBUG`
- **说明**: 日志级别（DEBUG显示详细信息，INFO显示基本信息）
- **示例**: `LOG_LEVEL=DEBUG`
- **可选值**: `DEBUG`、`INFO`、`WARNING`、`ERROR`

### LOG_DIR
- **类型**: 字符串
- **默认值**: `logs`
- **说明**: 日志保存目录
- **示例**: `LOG_DIR=logs`

### MAX_LOG_FILES
- **类型**: 整数
- **默认值**: `7`
- **说明**: 最大保留日志文件数量
- **示例**: `MAX_LOG_FILES=7`

### TIMING_MULTIPLIER
- **类型**: 浮点数
- **默认值**: `1.0`
- **说明**: 操作延迟倍数（0.5-3.0，数值越大操作越慢越像人类）
- **示例**: `TIMING_MULTIPLIER=1.0`
- **建议范围**: 0.5-3.0

### ENABLE_SMART_TIMING
- **类型**: 布尔值
- **默认值**: `true`
- **说明**: 是否启用智能延迟（根据页面复杂度自动调整延迟）
- **示例**: `ENABLE_SMART_TIMING=true`
- **可选值**: `true`、`false`

### MAX_RETRIES
- **类型**: 整数
- **默认值**: `3`
- **说明**: 最大重试次数
- **示例**: `MAX_RETRIES=3`
- **最小值**: 1次（强制限制）

### TIMEOUT_MINUTES
- **类型**: 整数
- **默认值**: `5`
- **说明**: 程序运行超时时间（分钟）
- **示例**: `TIMEOUT_MINUTES=5`
- **最小值**: 1分钟（强制限制）

---

## 🔄 配置优先级

配置加载的优先级顺序：

1. **环境变量** - 最高优先级
2. **config.env文件** - 次优先级
3. **代码默认值** - 最低优先级

### 本地运行
```bash
# 1. 复制配置模板
cp config.env.example config.env

# 2. 编辑配置文件
# 填写必要的配置项

# 3. 运行程序
python main.py
```

### GitHub Actions / CI环境
- 程序会自动使用环境变量
- 无需 config.env 文件
- 推荐在 Environment Secrets 中配置敏感信息

---

## ✅ 配置验证

程序启动时会自动验证以下配置：

### 必需配置验证
- `SITE_USERNAME` 和 `SITE_PASSWORD` 必须不为空
- 如果启用安全提问（`ENABLE_SECURITY_QUESTION=true`），必须设置 `SECURITY_ANSWER`
- 如果启用Telegram通知（`ENABLE_TELEGRAM_NOTIFICATION=true`），必须设置 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID`

### 数值范围验证
- `COMMENT_INTERVAL` 最小值为15秒
- `TIMEOUT_MINUTES` 最小值为1分钟
- `MAX_LOG_FILES` 必须为正整数

### 安全保护
- 敏感信息（密码、Token等）在日志中自动掩码处理
- 配置验证失败时程序会安全退出并显示错误信息

---

## 📝 配置示例

### 最小配置（仅签到）
```bash
# 必填
SITE_USERNAME=your_username
SITE_PASSWORD=your_password

# 可选（使用默认值）
ENABLE_CHECKIN=true
HEADLESS=true
```

### 完整配置（包含所有功能）
```bash
# 基础配置
SITE_USERNAME=your_username
SITE_PASSWORD=your_password
BASE_URL=https://www.sehuatang.org
ENABLE_CHECKIN=true

# 安全提问
ENABLE_SECURITY_QUESTION=false
SECURITY_QUESTION=您个人计算机的型号
SECURITY_ANSWER=your_answer

# Telegram通知
ENABLE_TELEGRAM_NOTIFICATION=true
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
TELEGRAM_SEND_LOG_FILE=true
TELEGRAM_SEND_SCREENSHOT=true

# 拟人化行为
ENABLE_REPLY=true
REPLY_COUNT=2
ENABLE_RANDOM_BROWSING=true
BROWSE_PAGE_COUNT=3
COMMENT_INTERVAL=15
WAIT_AFTER_LOGIN=5

# 高级配置
HEADLESS=true
LOG_LEVEL=DEBUG
TIMING_MULTIPLIER=1.0
ENABLE_SMART_TIMING=true
TIMEOUT_MINUTES=5
```

---

## 🔧 故障排除

### 🚨 常见配置错误

1. ❌ **用户名或密码错误**
   - 错误信息：`配置错误：请设置SITE_USERNAME和SITE_PASSWORD环境变量`
   - 解决方案：检查用户名和密码是否正确填写

2. ❌ **安全提问配置不完整**
   - 错误信息：`配置错误：启用安全提问功能需要设置SECURITY_ANSWER`
   - 解决方案：设置正确的安全提问答案

3. ❌ **Telegram配置不完整**
   - 错误信息：`配置错误：启用Telegram通知需要设置TELEGRAM_BOT_TOKEN和TELEGRAM_CHAT_ID`
   - 解决方案：正确配置Telegram机器人Token和聊天ID

### 🔧 配置调试技巧

1. 🐛 **使用调试模式**
   ```bash
   python main.py --debug
   ```

2. 🔍 **检查配置加载**
   - 程序启动时会显示已加载的配置（敏感信息已掩码）
   - 查看日志文件了解详细的配置加载过程

3. ✅ **验证配置文件**
   - 确保配置文件编码为UTF-8
   - 检查是否有多余的空格或特殊字符
   - 布尔值必须是 `true` 或 `false`（小写）
