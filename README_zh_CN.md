# ![阴阳的图标](resources/logo.svg) 阴阳

![](https://img.shields.io/github/v/release/oskarsh/yin-yang)
![](https://img.shields.io/github/v/release/oskarsh/yin-yang?include_prereleases)
![](https://img.shields.io/github/downloads/oskarsh/yin-yang/total)
![](https://img.shields.io/badge/Build%20with-Python-yellow)
![](https://img.shields.io/github/license/oskarsh/yin-yang)

适用于 Linux 的深色主题自动切换工具，支持诸如 KDE、Gnome 与 Budgie 等桌面环境以及 VSCode、Atom 等代码编辑器。

你可能也想看看我们的 [**讨论区**](https://github.com/oskarsh/Yin-Yang/discussions)，在那里我们讨论应用的未来以及其他有趣的事情！

> 翻译:[🇹🇼](README_zh_TW.md) [🇨🇳](README_zh_CN.md)

![应用效果预览](.github/images/header.png)
![应用设置界面](.github/images/settings.png)

## 特性

* 可以根据时间更换深色（或浅色）主题
* 支持桌面环境：
  * Gnome
  * Budgie
  * KDE Plasma
* 支持应用程序：
  * VSCode、Atom、gedit
  * Firefox、Brave
  * Kvantum
  * Konsole
  * OnlyOffice
  * 以及更多……
* 其他功能：
  * 更换壁纸
  * 更换主题时发送通知
  * 播放提示音
  * 可以运行自定义脚本

> 想要了解更多计划中的功能以及开发状态，请访问[项目状态页面](https://github.com/oskarsh/Yin-Yang/projects?type=classic)。

## 安装

### 基于 Arch 的发行版
Yin-Yang 可以从 AUR 下载，包名为 [yin-yang](https://aur.archlinux.org/packages/yin-yang)。

### 从源码安装
Yin-Yang 依赖于 pypi 上的 `python-systemd` 和 `pyside6`。`python-systemd` 需要你已经安装了 systemd-headers。你还需要安装 Python 开发头文件（例如 `python3-devel`）。

对于 CentOS、RHEL 和 Fedora：
```bash
sudo dnf install gcc systemd-devel python3-devel libnotify
```

对于 OpenSUSE：
```bash
sudo zypper refresh
sudo zypper install gcc systemd-devel libnotify
```

对于 Debian、Ubuntu 等：
```bash
sudo apt update
sudo apt install libsystemd-dev gcc pkg-config python3-dev libnotify-bin
```

然后你可以在 Python 虚拟环境中安装 Yin-Yang：
```bash
# bash 是必需的，用于运行 source 命令
bash
# 克隆代码到你的本地机器
git clone https://github.com/oskarsh/Yin-Yang.git
cd Yin-Yang
# 安装 Yin-Yang
./scripts/install.sh
```

对于开发，跳过安装步骤，而是在你的家目录中创建一个虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # 这是 bash 的命令，其他 shell 中也有类似的脚本，例如 fish
pip install -r requirements.txt
```

## 文档

想要帮助？查看 Wiki 以了解如何贡献翻译、插件等！

[![Generic badge](https://img.shields.io/badge/Visit-Wiki-BLUE.svg)](<https://github.com/oskarsh/Yin-Yang/wiki>)

## 相关或类似的项目

- Windows 的自动深色模式：https://github.com/AutoDarkMode/Windows-Auto-Night-Mode
- Gnome 的自动深色模式扩展：https://extensions.gnome.org/extension/2236/night-theme-switcher/
- Jetbrains IDE 的自动深色模式：https://github.com/weisJ/auto-dark-mode
- 与 KDE 的夜间颜色同步深色模式：https://github.com/adrium/knightadjuster
- darkman：https://gitlab.com/WhyNotHugo/darkman
- 在 Firefox 中，你可以使用系统主题来同步 Firefox 本身和支持的应用程序的主题。当你使用 [dark reader](https://darkreader.org/) 时，你可以启用系统颜色自动化。

## 感谢所有为本项目做出贡献的人❤

### 编程

本项目由诸多开源志愿者用爱浇灌而成。

[参与社区贡献](https://github.com/oskarsh/Yin-Yang/wiki/Contributing)

[![](https://opencollective.com/Yin-Yang/contributors.svg?button=false)](https://github.com/oskarsh/Yin-Yang/graphs/contributors)

### 资金支持

<a href="https://opencollective.com/Yin-Yang/organization/0/website"><img src="https://opencollective.com/Yin-Yang/organization/0/avatar.svg"></a>
<a href="https://opencollective.com/Yin-Yang/organization/1/website"><img src="https://opencollective.com/Yin-Yang/organization/1/avatar.svg"></a>
<a href="https://opencollective.com/Yin-Yang/organization/2/website"><img src="https://opencollective.com/Yin-Yang/organization/2/avatar.svg"></a>
<a href="https://opencollective.com/Yin-Yang/organization/3/website"><img src="https://opencollective.com/Yin-Yang/organization/3/avatar.svg"></a>
<a href="https://opencollective.com/Yin-Yang/organization/4/website"><img src="https://opencollective.com/Yin-Yang/organization/4/avatar.svg"></a>
<a href="https://opencollective.com/Yin-Yang/organization/5/website"><img src="https://opencollective.com/Yin-Yang/organization/5/avatar.svg"></a>
<a href="https://opencollective.com/Yin-Yang/organization/6/website"><img src="https://opencollective.com/Yin-Yang/organization/6/avatar.svg"></a>
<a href="https://opencollective.com/Yin-Yang/organization/7/website"><img src="https://opencollective.com/Yin-Yang/organization/7/avatar.svg"></a>
<a href="https://opencollective.com/Yin-Yang/organization/8/website"><img src="https://opencollective.com/Yin-Yang/organization/8/avatar.svg"></a>
<a href="https://opencollective.com/Yin-Yang/organization/9/website"><img src="https://opencollective.com/Yin-Yang/organization/9/avatar.svg"></a>
