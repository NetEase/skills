---
name: ncm-cli-setup
description: 安装和配置 ncm-cli（网易云音乐 CLI 工具）。当用户需要安装 ncm-cli、配置 API Key、安装 mpv 播放器，或排查安装问题时，使用此 skill。
---

# ncm-cli 安装配置

ncm-cli 是网易云音乐的 CLI 工具（音乐搜索、播放控制、歌单管理、TUI 播放器）。

## 安装流程

### 第一步：安装 ncm-cli、mpv

#### 1.1 安装 ncm-cli

```bash
npm install -g @music163/ncm-cli
```

验证安装：

```bash
ncm-cli --version
```

#### 1.2 安装 mpv

播放功能需要 mpv 播放器。先检测是否已安装：

```bash
mpv --version
```

**macOS / Windows**：若未安装，直接执行安装脚本：

```bash
python3 scripts/install_mpv.py
```

**Linux**：询问用户是否需要播放功能：

- 如果是桌面环境、需要本地播放 → 执行 `python3 scripts/install_mpv.py`
- 如果是服务器环境、不需要播放 → 跳过，搜索/歌单等命令仍可正常使用

安装脚本会自动识别包管理器：

- **macOS**：Homebrew（`brew install mpv`）或 MacPorts
- **Linux**：apt / dnf / pacman / zypper
- **Windows**：winget / Chocolatey / Scoop

### 第二步：配置 API Key

使用 ncm-cli 需要先设置API Key：

```bash
ncm-cli config set appId <你的AppId>
ncm-cli config set privateKey <你的PrivateKey>
```

> 如果还没有 API Key，请先前往[网易云音乐开放平台](https://developer.music.163.com/st/developer/apply/account?type=INDIVIDUAL)申请 API Key（appId 和
> privateKey）。

### 第三步：配置默认播放器

询问用户选择默认播放器：

- **mpv**（内置播放器）：轻量、跨平台，需先完成第一步中的 mpv 安装
- **orpheus**（云音乐 App）：调用本地网易云音乐客户端播放，仅支持 macOS

根据用户选择执行：

```bash
ncm-cli config set player mpv      # 选择内置播放器
ncm-cli config set player orpheus  # 选择云音乐 App
```

### 第四步：登录

登录是必须的，请使用：

```bash
ncm-cli login --background
```

## 常见问题

| 问题                           | 解决方法                                                       |
|------------------------------|------------------------------------------------------------|
| `ncm-cli: command not found` | 检查 npm 全局 bin 是否在 PATH 中：`npm bin -g`                      |
| `mpv not found`              | 重新运行 `python3 scripts/install_mpv.py` 或手动安装：https://mpv.io |
| 登录超时                         | 重新执行 `ncm-cli login --background`                          |

## 基本信息

- 需要 **Node.js >= 18**
