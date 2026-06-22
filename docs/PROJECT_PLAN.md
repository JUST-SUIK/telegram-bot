# Telegram Bot Agent — 项目计划文档

> 创建日期：2026-06-22
> 状态：规划阶段，架构待确认

---

## 一、项目概述

### 1.1 一句话描述

通过 Telegram Bot 实现手机远程监控和操控电脑上的软件，让 Telegram 成为电脑的"AI 代理遥控器"。

### 1.2 核心价值

- **随时掌控**：离开电脑后，用手机就能知道软件运行状态
- **主动通知**：异常发生时 Bot 主动推送，不用一直盯着
- **远程操作**：通过聊天消息代替鼠标键盘操作电脑
- **AI 代理**：结合 Claude Code CLI，让 AI 帮你分析问题、执行操作

---

## 二、需求分析

### 2.1 需求背景

在日常开发中，经常遇到以下场景：

1. **长时间任务**：训练模型、跑测试、编译大项目，需要等很长时间，但又不想一直坐在电脑前
2. **多软件协同**：同时跑好几个工具，需要知道每个的进度
3. **远程办公**：出门在外，突然想知道电脑上的任务进展如何
4. **紧急响应**：软件报错或需要人工确认，希望第一时间知道并处理

### 2.2 当前痛点

| 痛点 | 具体表现 |
|------|----------|
| 被迫守在电脑前 | 长时间任务必须在旁边等，离开就不知道情况 |
| 信息碎片化 | 不同软件的日志、状态分散在各处，没法统一查看 |
| 响应不及时 | 出门后发现软件卡住或报错，只能等回来再处理 |
| 操作不便 | 只想点个"确认"或看下进度，却要远程桌面连回去 |
| 现有工具不合适 | 远程桌面太重、TeamViewer 连接慢、SSH 看不了 GUI |

### 2.3 核心需求（按优先级）

#### P0 — 必须实现

| 需求 | 描述 | 用户场景 |
|------|------|----------|
| 进程监控 | 查看指定软件是否在运行、CPU/内存占用 | "VSCode 还在跑吗？占了多少内存？" |
| 日志读取 | 读取软件的最近日志输出 | "把最新的错误日志发给我" |
| 命令执行 | 在电脑上执行命令行命令 | "帮我重启一下那个服务" |
| 截图 | 截取当前屏幕或指定窗口 | "截个图让我看看现在什么情况" |
| 主动通知 | 进程退出或资源异常时自动推送 | 软件崩溃了自动发消息告诉你 |

#### P1 — 重要功能

| 需求 | 描述 | 用户场景 |
|------|------|----------|
| GUI 自动化 | 模拟鼠标点击和键盘输入 | "帮我点那个确认按钮" |
| Claude Code 集成 | 调用 Claude Code CLI 进行 AI 问答和代码操作 | "帮我看看这段代码有什么问题" |
| 多软件管理 | 同时监控和管理多个软件 | "列一下当前在跑的所有程序" |

#### P2 — 增强功能

| 需求 | 描述 | 用户场景 |
|------|------|----------|
| 语音指令 | 发语音消息，转文字后执行 | 开车时发语音说"帮我看看训练进度" |
| 定时任务 | 定时检查并汇报状态 | "每 30 分钟给我发一次训练进度" |
| VSCode 深度集成 | 和 VSCode 中的 Claude Code 扩展交互 | "问下 VSCode 里的 Claude 帮我改的代码改完没" |

---

## 三、问题定义

### 3.1 要解决的核心问题

**如何在手机上用最少的操作，获取电脑软件的运行状态并进行远程干预？**

### 3.2 为什么选择 Telegram Bot

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| Telegram Bot | API 成熟、通知可靠、跨平台、免费、开发简单 | 国内需要代理 | ✅ 首选 |
| 微信 Bot | 国内普及 | 官方 API 限制多、容易封号 | ❌ |
| 钉钉/飞书 Bot | 国内可用、企业场景好 | 个人使用体验差、功能受限 | ❌ |
| 自建 Web 界面 | 完全自控 | 需要部署服务器、手机浏览器体验差、需要自己做通知 | ❌ |
| 远程桌面 | 能看到完整画面 | 太重、延迟高、手机操作不便 | ❌ |

### 3.3 关键设计决策（待确认）

- [ ] 消息通道：Telegram（推荐） vs 其他
- [ ] 运行环境：Windows 原生（推荐） vs WSL
- [ ] AI 后端：Claude Code CLI（推荐） vs Claude API 直接调用
- [ ] GUI 自动化：pyautogui vs pywinauto vs 其他
- [ ] 截图方案：PIL.ImageGrab vs mss vs Windows API

---

## 四、解决方案

### 4.1 整体思路

```
手机 Telegram ←→ Telegram Bot Server ←→ PC Agent 能力层 ←→ 电脑软件
```

**核心理念**：把"看屏幕、点鼠标、敲键盘"变成"发消息、收结果"。

### 4.2 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                     手机 Telegram App                        │
│  用户发消息：/status、/screenshot、/click 100,200、/ask ...   │
└──────────────────────────┬──────────────────────────────────┘
                           │ Telegram Bot API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Telegram Bot Server                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ 消息解析器   │  │ 权限管理     │  │ 消息队列/任务调度    │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         └────────────────┼────────────────────┘             │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Agent 能力层                          ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐││
│  │  │ 进程监控  │ │ 日志读取  │ │ 命令执行  │ │ 截图       │││
│  │  │ psutil   │ │ tail/log │ │ subprocess│ │ PIL/mss    │││
│  │  └──────────┘ └──────────┘ └──────────┘ └────────────┘││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐││
│  │  │ GUI自动化 │ │ 文件操作  │ │ Claude   │ │ 通知推送   │││
│  │  │ pyautogui│ │ pathlib  │ │ CLI 调用  │ │ 主动告警   │││
│  │  └──────────┘ └──────────┘ └──────────┘ └────────────┘││
│  └─────────────────────────────────────────────────────────┘│
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      电脑本地环境                             │
│  VSCode / Claude Code / 训练脚本 / 其他软件                   │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 技术栈选型（待确认）

| 层级 | 技术选择 | 备选方案 | 选择理由 |
|------|----------|----------|----------|
| 语言 | Python 3.11+ | Node.js | 生态成熟，系统操作库丰富 |
| Telegram SDK | python-telegram-bot | telegraf (Node) | Python 官方推荐，文档完善 |
| 进程监控 | psutil | wmi | 跨平台，API 简洁 |
| 截图 | mss | PIL.ImageGrab / pyautogui | 速度快，支持多显示器 |
| GUI 自动化 | pyautogui + pywinauto | Selenium (仅网页) | pyautogui 通用，pywinauto 更精准 |
| AI 后端 | Claude Code CLI (subprocess) | Anthropic API | CLI 可以操作文件和代码，能力更强 |
| 语音转文字 | OpenAI Whisper API | 本地 whisper | API 简单，质量好 |
| 配置管理 | .env + YAML | JSON / TOML | YAML 可读性好，适合复杂配置 |
| 日志 | Python logging + 文件轮转 | — | 标准库，够用 |

### 4.4 功能详细设计

#### 命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| `/start` | 启动 Bot，显示欢迎信息 | |
| `/help` | 显示所有命令说明 | |
| `/status` | 显示所有监控中的进程状态 | |
| `/status <进程名>` | 显示指定进程的详细状态 | `/status code` |
| `/log <进程名> [行数]` | 读取最近 N 行日志 | `/log training 50` |
| `/screenshot` | 截取当前全屏 | |
| `/screenshot <窗口名>` | 截取指定窗口 | `/screenshot VSCode` |
| `/click <x,y>` | 在屏幕坐标 (x,y) 处点击 | `/click 500,300` |
| `/type <文本>` | 输入文本 | `/type hello world` |
| `/key <按键>` | 按下指定键 | `/key enter` |
| `/exec <命令>` | 执行系统命令 | `/exec dir` |
| `/ask <问题>` | 调用 Claude Code 问答 | `/ask 这段代码有什么bug` |
| `/monitor <进程名>` | 添加监控目标 | `/monitor python` |
| `/unmonitor <进程名>` | 移除监控目标 | `/unmonitor python` |
| `/watch <秒>` | 设置监控间隔 | `/watch 60` |
| `/list` | 列出当前所有运行中的进程 | |

#### 自动监控机制

```python
# 伪代码：监控循环
while True:
    for target in monitored_targets:
        status = check_process(target)
        if status.changed:
            if status.exited:
                send_alert(f"⚠️ {target} 已退出，退出码：{status.exit_code}")
            elif status.high_cpu:
                send_alert(f"🔥 {target} CPU 占用 {status.cpu}%")
            elif status.high_memory:
                send_alert(f"💾 {target} 内存占用 {status.memory}%")
    sleep(monitor_interval)
```

#### 安全设计

| 风险 | 防护措施 |
|------|----------|
| 未授权访问 | 用户白名单（ALLOWED_USER_IDS），只允许指定用户操作 |
| 危险命令 | 命令黑名单（rm -rf, format 等），敏感操作需二次确认 |
| API Key 泄露 | 所有密钥存 .env，不提交到 git |
| 资源滥用 | 命令执行超时限制，防止死循环 |
| 操作审计 | 所有操作记录日志，包含时间、用户、命令、结果 |

---

## 五、项目结构（待确认）

```
telegram-bot/
├── docs/
│   └── PROJECT_PLAN.md          # 本文档
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── main.py              # Bot 入口，启动和配置
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── status.py        # /status 命令处理
│   │   │   ├── screenshot.py    # /screenshot 命令处理
│   │   │   ├── command.py       # /exec 命令处理
│   │   │   ├── gui.py           # /click /type /key 处理
│   │   │   ├── log.py           # /log 命令处理
│   │   │   ├── claude.py        # /ask 命令处理
│   │   │   └── monitor.py       # /monitor /unmonitor 处理
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── process.py       # 进程监控服务
│   │   │   ├── screenshot.py    # 截图服务
│   │   │   ├── gui_auto.py      # GUI 自动化服务
│   │   │   ├── executor.py      # 命令执行服务
│   │   │   ├── claude_cli.py    # Claude Code CLI 封装
│   │   │   └── notifier.py      # 通知推送服务
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── config.py        # 配置管理
│   │       ├── security.py      # 安全检查
│   │       └── logger.py        # 日志工具
│   └── config/
│       ├── config.yaml          # 主配置文件
│       └── .env.example         # 环境变量模板
├── tests/
│   ├── test_handlers/
│   └── test_services/
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── run.py                       # 启动脚本
```

---

## 六、配置文件设计（待确认）

### config.yaml

```yaml
# Telegram Bot 配置
telegram:
  token: ${TELEGRAM_BOT_TOKEN}    # 从 .env 读取
  allowed_users:                   # 允许使用的 Telegram 用户 ID
    - 123456789
  proxy:                           # 代理配置（国内可能需要）
    enabled: false
    url: "socks5://127.0.0.1:7890"

# 监控配置
monitor:
  interval: 60                     # 监控间隔（秒）
  targets:                         # 默认监控目标
    - name: "VSCode"
      process: "Code.exe"
      alert_on_exit: true
      alert_cpu_threshold: 80      # CPU 超过 80% 告警
      alert_memory_threshold: 80   # 内存超过 80% 告警
    - name: "Python训练"
      process: "python.exe"
      log_path: "./logs/training.log"
      alert_on_exit: true

# 截图配置
screenshot:
  max_width: 1920                  # 最大宽度，超过自动缩放
  format: "png"                    # png 或 jpg
  quality: 85                      # jpg 质量

# GUI 自动化配置
gui:
  confirm_before_click: true       # 点击前是否需要确认
  click_delay: 0.5                 # 点击后延迟（秒）

# Claude Code 配置
claude:
  cli_path: "claude"               # Claude Code CLI 路径
  timeout: 120                     # 命令超时（秒）
  working_dir: "E:/Project"        # 默认工作目录

# 命令执行配置
executor:
  timeout: 30                      # 命令超时（秒）
  blacklist:                       # 命令黑名单
    - "rm -rf"
    - "format"
    - "shutdown"
    - "del /f /s /q"

# 日志配置
logging:
  level: "INFO"
  file: "./logs/bot.log"
  max_size: 10                     # MB
  backup_count: 5
```

---

## 七、实施计划

### 阶段一：基础框架（预计 1-2 天）

- [ ] 搭建项目结构
- [ ] 实现 Telegram Bot 基础框架
- [ ] 实现配置管理
- [ ] 实现 `/start`、`/help` 命令
- **验证**：Bot 能启动，能回复消息

### 阶段二：监控能力（预计 1 天）

- [ ] 实现进程监控服务（psutil）
- [ ] 实现 `/status`、`/list` 命令
- [ ] 实现主动告警通知
- **验证**：能看到进程状态，异常时收到通知

### 阶段三：远程操作（预计 1-2 天）

- [ ] 实现命令执行服务
- [ ] 实现截图服务
- [ ] 实现 `/exec`、`/screenshot`、`/log` 命令
- **验证**：能执行命令、截屏、读日志

### 阶段四：GUI 自动化（预计 1 天）

- [ ] 实现鼠标点击、键盘输入
- [ ] 实现 `/click`、`/type`、`/key` 命令
- [ ] 添加安全确认机制
- **验证**：能远程点击按钮、输入文字

### 阶段五：AI 集成（预计 1 天）

- [ ] 实现 Claude Code CLI 调用
- [ ] 实现 `/ask` 命令
- **验证**：能通过 Telegram 向 Claude 提问并收到回答

### 阶段六：增强功能（预计 1-2 天）

- [ ] 语音消息转文字
- [ ] 定时监控任务
- [ ] Windows 开机自启
- [ ] 完善文档

---

## 八、待确认事项

以下技术细节需要在开发前确认：

### 8.1 架构选择

- [ ] **运行环境**：Windows 原生（推荐） vs WSL
  - Windows 原生：pyautogui 截图和 GUI 控制更直接
  - WSL：claude-telegram-bot-bridge 可以直接用，但 GUI 操作受限

- [ ] **AI 后端**：Claude Code CLI vs Anthropic API
  - CLI：可以操作文件、执行命令，能力更强
  - API：只能对话，但响应更快、更稳定

### 8.2 技术细节

- [ ] **截图方案**：mss vs PIL.ImageGrab vs pyautogui
  - mss：速度快，支持多显示器
  - PIL.ImageGrab：简单，但多显示器支持差
  - pyautogui：和 GUI 自动化统一，但速度一般

- [ ] **GUI 自动化**：pyautogui vs pywinauto
  - pyautogui：坐标点击，通用但不精准
  - pywinauto：控件识别，精准但学习成本高

- [ ] **Telegram 代理**：是否需要配置代理
  - 国内访问 Telegram 需要代理
  - 需要确认你的代理软件和端口

### 8.3 安全相关

- [ ] 确认允许使用的 Telegram 用户 ID
- [ ] 确认命令执行的黑名单范围
- [ ] 确认是否需要操作二次确认

---

## 九、参考资料

### 现有开源项目

| 项目 | 地址 | 参考价值 |
|------|------|----------|
| claude-telegram-bot-bridge | https://github.com/terranc/claude-telegram-bot-bridge | Claude Code CLI 集成方式 |
| python-telegram-bot | https://github.com/python-telegram-bot/python-telegram-bot | Telegram SDK 用法 |
| psutil | https://github.com/giampaolo/psutil | 进程监控 API |
| pyautogui | https://github.com/asweigart/pyautogui | GUI 自动化 |

### 文档

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot 文档](https://docs.python-telegram-bot.org/)
- [psutil 文档](https://psutil.readthedocs.io/)
- [Claude Code CLI 文档](https://docs.anthropic.com/claude-code)

---

*本文档将随项目推进持续更新。*
