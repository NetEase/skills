#!/usr/bin/env python3
"""
Cross-platform mpv installer for ncm-cli.
Detects OS and installs mpv using the appropriate package manager.
"""

import sys
import subprocess
import shutil
import platform


def run(cmd, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result


def check_mpv():
    return shutil.which("mpv") is not None


def check_audio_support():
    """检测 Linux 系统是否有可用的音频输出设备，其他平台直接返回 True"""
    if platform.system().lower() != "linux":
        return True
    # 优先检查 PulseAudio/PipeWire
    if shutil.which("pactl"):
        result = run("pactl list sinks short", check=False)
        if result.returncode == 0 and result.stdout.strip():
            return True
    # 回退到 ALSA
    if shutil.which("aplay"):
        result = run("aplay -l", check=False)
        return result.returncode == 0 and "card" in result.stdout
    # 检查 /proc/asound 是否有声卡
    try:
        with open("/proc/asound/cards") as f:
            return "no soundcards" not in f.read()
    except FileNotFoundError:
        pass
    return False


def install_macos():
    if shutil.which("brew"):
        print("Installing mpv via Homebrew...")
        run("brew install mpv")
    elif shutil.which("port"):
        print("Installing mpv via MacPorts...")
        run("sudo port install mpv")
    else:
        print("ERROR: Neither Homebrew nor MacPorts found.")
        print("Install Homebrew first: https://brew.sh")
        print("Then run: brew install mpv")
        sys.exit(1)


def install_linux():
    # Detect distro
    distro = ""
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    distro = line.strip().split("=", 1)[1].strip('"').lower()
                    break
    except FileNotFoundError:
        pass

    if distro in ("ubuntu", "debian", "linuxmint", "pop"):
        print("Installing mpv via apt...")
        run("sudo apt-get update -q && sudo apt-get install -y mpv")
    elif distro in ("fedora",):
        print("Installing mpv via dnf...")
        run("sudo dnf install -y mpv")
    elif distro in ("centos", "rhel", "rocky", "almalinux"):
        print("Installing mpv via yum (requires EPEL)...")
        run("sudo yum install -y epel-release && sudo yum install -y mpv")
    elif distro in ("arch", "manjaro", "endeavouros"):
        print("Installing mpv via pacman...")
        run("sudo pacman -S --noconfirm mpv")
    elif distro in ("opensuse", "opensuse-leap", "opensuse-tumbleweed", "sles"):
        print("Installing mpv via zypper...")
        run("sudo zypper install -y mpv")
    elif shutil.which("apt-get"):
        print("Detected apt-based system. Installing mpv via apt...")
        run("sudo apt-get update -q && sudo apt-get install -y mpv")
    elif shutil.which("dnf"):
        print("Detected dnf. Installing mpv via dnf...")
        run("sudo dnf install -y mpv")
    elif shutil.which("pacman"):
        print("Detected pacman. Installing mpv via pacman...")
        run("sudo pacman -S --noconfirm mpv")
    else:
        print("ERROR: Could not detect package manager.")
        print("Please install mpv manually: https://mpv.io/installation/")
        sys.exit(1)


def install_windows():
    if shutil.which("winget"):
        print("Installing mpv via winget...")
        run("winget install mpv.mpv")
    elif shutil.which("choco"):
        print("Installing mpv via Chocolatey...")
        run("choco install mpv -y")
    elif shutil.which("scoop"):
        print("Installing mpv via Scoop...")
        run("scoop install mpv")
    else:
        print("ERROR: No supported package manager found (winget / choco / scoop).")
        print("Download mpv from https://mpv.io/installation/ and add it to PATH.")
        sys.exit(1)


def main():
    print("=== mpv installer for ncm-cli ===\n")

    if check_mpv():
        result = run("mpv --version", check=False)
        version_line = result.stdout.splitlines()[0] if result.stdout else "unknown"
        print(f"mpv is already installed: {version_line}")
        print("No action needed.")
        return

    print("Checking audio support...")
    if not check_audio_support():
        print("No audio output device detected. Skipping mpv installation.")
        return

    print("Audio support detected. Installing mpv...\n")
    os_name = platform.system().lower()

    if os_name == "darwin":
        install_macos()
    elif os_name == "linux":
        install_linux()
    elif os_name == "windows":
        install_windows()
    else:
        print(f"ERROR: Unsupported OS: {os_name}")
        print("Please install mpv manually: https://mpv.io/installation/")
        sys.exit(1)

    if check_mpv():
        print("\nmpv installed successfully!")
    else:
        print("\nWARNING: mpv still not found in PATH after installation.")
        print("You may need to restart your terminal or add mpv to PATH.")


if __name__ == "__main__":
    main()
