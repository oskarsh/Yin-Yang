# ![Yin & Yang logo](resources/logo.svg) Yin-Yang

![](https://img.shields.io/github/v/release/oskarsh/yin-yang)
![](https://img.shields.io/github/v/release/oskarsh/yin-yang?include_prereleases)
![](https://img.shields.io/github/downloads/oskarsh/yin-yang/total)
![](https://img.shields.io/badge/Build%20with-Python-yellow)
![](https://img.shields.io/github/license/oskarsh/yin-yang)

Linux 的自動化主題管理員，支援 KDE、Gnome、Budgie 等桌面環境 
還可以自動設定 VSCode、Atom 等應用程式的主題。

安裝後可以查看我們的[**論壇**](https://github.com/oskarsh/Yin-Yang/discussions)，會有好康的！

> 翻譯：[ 🇺🇸](README.md) [🇨🇳](README_zh_CN.md)

![Visualization](.github/images/header.png)
![App configuration](.github/images/settings.png)

## 功能

* 在自訂時間或是依照日出日落自動切換主題
* 支援的桌面環境：
  * Gnome
  * Budgie
  * KDE Plasma
* 支援的應用程式：
  * VSCode、Atom、gedit
  * Firefox、Brave
  * Kvantum
  * Konsole
  * OnlyOffice
  * 等等...
* 其他
  * 自動更換桌布
  * 自動推送通知
  * 切換主題時播放聲音
  * 自動執行腳本

> 想看 ETA 的人可以查看[進度](https://github.com/oskarsh/Yin-Yang/projects?type=classic).

## 安裝

### Arch（BTW）系列
Yin-Yang 可從 AUR 套件 [`yin-yang`](https://aur.archlinux.org/packages/yin-yang) 安裝


### 自行編譯
Yin-Yang 依賴 `python-systemd` 以及 `pyside6` 等 Pypi。`python-systemd` 依賴 systemd-headers 以及 `python3-devel` 等。

CentOS、RHEL、Fedora：
```bash
sudo dnf install gcc systemd-devel python3-devel libnotify
``` 

OpenSUSE：
```bash
sudo zypper refresh
sudo zypper install gcc systemd-devel libnotify
```

Debian 系列：
```bash
sudo apt update
sudo apt install libsystemd-dev gcc pkg-config python3-dev libnotify-bin
```

接下來請安裝 Yin-Yang 至虛擬 python 環境：
```bash
# bash 是建議的 shell
bash
# 克隆原始碼
git clone https://github.com/oskarsh/Yin-Yang.git
cd Yin-Yang
# 安裝 Yin-Yang
./scripts/install.sh
```

開發者請略過安裝並且在家目錄中建立 vnev 資料夾
```bash
python -m venv .venv
source .venv/bin/activate  # 此腳本是為了 bash 設計，若使用其他殼層，請在同個資料夾中尋找相容的腳本
pip install -r requirements.txt
```

## 說明

想要為此軟體貢獻？請查看維基尋找如何翻譯此軟體、或擴充功能等等！

[![Generic badge](https://img.shields.io/badge/Visit-Wiki-BLUE.svg)](<https://github.com/oskarsh/Yin-Yang/wiki>)

## 其他相似軟體

- Windows 的自動暗黑模式[Windows Auto Night Mode](https://github.com/AutoDarkMode/Windows-Auto-Night-Mode)
- Gnome 的自動暗黑模式[Night Theme Switcher](https://extensions.gnome.org/extension/2236/night-theme-switcher/)
- Jetbrains IDE 自動暗黑模式 [Auto Dark Mode](https://github.com/weisJ/auto-dark-mode)
- 自動化 KDE 藍光濾鏡 [Knight Adjuster](https://github.com/adrium/knightadjuster)
- [darkman](https://gitlab.com/WhyNotHugo/darkman)
- Firefox 的自動暗黑模式 [dark reader](https://darkreader.org/)

## 感謝所有貢獻者！

### 軟體貢獻者

感謝你們！因為有這些貢獻者才有這個軟體的出現！[[貢獻](https://github.com/oskarsh/Yin-Yang/wiki/Contributing)].

[![](https://opencollective.com/Yin-Yang/contributors.svg?button=false)](https://github.com/oskarsh/Yin-Yang/graphs/contributors)

### 捐獻

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