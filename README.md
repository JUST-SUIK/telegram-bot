# Telegram Bot Agent

通过 Telegram Bot 实现手机远程监控和操控电脑的 AI 代理工具。

## 功能特性

- 📊 **进程监控**: 查看运行中的进程状态、CPU/内存占用
- 📸 **远程截图**: 截取电脑屏幕并发送到手机
- ⌨️ **命令执行**: 远程执行系统命令
- 🖱️ **GUI 自动化**: AI 辅助识别并点击按钮、输入文字
- 🤖 **AI 问答**: 调用 Claude Code CLI 进行代码分析

## 快速开始

### 方式一：GUI 管理面板（推荐）

双击运行 `启动Bot管理器.bat`，打开可视化管理面板：

- 📊 仪表盘：一键启动/停止 Bot、查看运行状态
- ⚙️ 配置：编辑 .env 配置文件
- 📝 日志：实时查看运行日志
- 🖥️ 进程：查看系统进程和资源使用

### 方式二：命令行启动

### 前置要求

- Windows 10/11
- Python 3.11+
- Telegram Bot Token
- MiMo API Key

### 安装

1. 克隆项目
```bash
git clone <repository-url>
cd telegram-bot
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

4. 运行
```bash
python run.py
```

### 打包成 exe

```bash
python build.py
```

生成的可执行文件在 `dist/telegram_bot_agent.exe`

## 命令列表

| 命令 | 说明 | 示例 |
|------|------|------|
| `/start` | 显示欢迎信息 | |
| `/help` | 显示帮助 | |
| `/status` | 查看进程状态 | `/status python` |
| `/list` | 列出运行中的进程 | |
| `/screenshot` | 截取屏幕 | |
| `/exec` | 执行命令 | `/exec dir` |
| `/ask` | AI 问答 | `/ask 这段代码有什么问题？` |
| `/click` | 点击元素 | `/click 确认按钮` |
| `/type` | 输入文字 | `/type hello` |
| `/key` | 按下按键 | `/key enter` |

## 配置说明

### 环境变量 (.env)

```env
TELEGRAM_BOT_TOKEN=your_token
MIMO_API_KEY=your_api_key
MIMO_API_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
PROXY_URL=socks5://127.0.0.1:7897
ALLOWED_USER_IDS=6531095340
```

### 配置文件 (src/config/config.yaml)

详见 `src/config/config.yaml` 中的注释

## 安全特性

- ✅ 用户白名单验证（所有命令都需要授权）
- ✅ 命令黑名单过滤（防止危险命令执行）
- ✅ 危险操作二次确认（GUI 点击操作需要确认）
- ✅ 操作日志记录
- ✅ 代理配置支持（Clash Verge）
- ✅ pyautogui FAILSAFE 启用（鼠标移到角落可紧急停止）

## 技术栈

- Python 3.11+
- python-telegram-bot
- psutil
- mss
- pyautogui
- MiMo API (OpenAI 兼容)

## 许可证

MIT License