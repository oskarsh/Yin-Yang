# ![Yin & Yang logo](resources/logo.svg) Yin-Yang

![](https://img.shields.io/github/v/release/oskarsh/yin-yang)
![](https://img.shields.io/github/v/release/oskarsh/yin-yang?include_prereleases)
![](https://img.shields.io/github/downloads/oskarsh/yin-yang/total)
![](https://img.shields.io/badge/Build%20with-Python-yellow)
![](https://img.shields.io/github/license/oskarsh/yin-yang)

Auto Night-mode for Linux, it supports popular Desktops like KDE, Gnome, Budgie 
and also themes your favourite editors like VSCode or Atom.

You might also want to take a look at our [**discussions page**](https://github.com/oskarsh/Yin-Yang/discussions), where we talk about the future of the app and other cool stuff!

> Translations: [🇨🇳](README_zh.md)

![Visualization](.github/images/header.png)
![App configuration](.github/images/settings.png)

## Features

* Changes your themes at certain times or sunrise and sunset
* Supported Desktops:
  * Gnome
  * Budgie
  * KDE Plasma
* Supported applications:
  * VSCode, Atom, gedit
  * Firefox & Brave
  * Kvantum
  * Konsole
  * OnlyOffice
  * and more...
* Miscellaneous:
  * Wallpaper change
  * Notifications on theme change
  * Play a sound
  * Ability to run custom scripts

> To see planned features and the development status, visit the [project status page](https://github.com/oskarsh/Yin-Yang/projects?type=classic).

## Installation

### Arch-based distributions
Yin-Yang can be downloaded from AUR as [yin-yang](https://aur.archlinux.org/packages/yin-yang) package.


### Source
Yin-Yang depends on `python-systemd` and `pyside6` from pypi. `python-systemd` requires you have installed the systemd-headers from your package manager. You also need python development headers (e.g. `python3-devel`).

For CentOS, RHEL, and Fedora:
```bash
sudo dnf install gcc systemd-devel
``` 

For Debian, Ubuntu, etc.
```bash
sudo apt update
sudo apt install libsystemd-dev gcc pkg-config python3-dev
```

Then you can install Yin-Yang in a python virtual environemnt:
```bash
git clone https://github.com/oskarsh/Yin-Yang && cd Yin-Yang
## Create virtual environment for pypi packages
python3 -m venv .venv
source .venv/bin/activate
# Install pip requirements
pip3 install -r requirements.txt
# Install Yin-Yang
./scripts/install.sh
```

## Documentation

Want to help out? Check out the wiki to learn how to contribute translations, plugins and more!

[![Generic badge](https://img.shields.io/badge/Visit-Wiki-BLUE.svg)](<https://github.com/oskarsh/Yin-Yang/wiki>)

## Related or similar projects

- Auto dark mode for Windows: https://github.com/AutoDarkMode/Windows-Auto-Night-Mode
- Auto dark mode extension for Gnome: https://extensions.gnome.org/extension/2236/night-theme-switcher/
- Auto dark mode for Jetbrains IDEs: https://github.com/weisJ/auto-dark-mode
- Sync dark mode with KDEs night color: https://github.com/adrium/knightadjuster
- darkman: https://gitlab.com/WhyNotHugo/darkman
- In Firefox, you can use the system theme to sync Firefox itself and supported applications with the theme of the system. When you use [dark reader](https://darkreader.org/), you can enable the system color automation.

## Thanks to all Contributors

### Code Contributors

This project exists thanks to all the people who contribute. [[Contribute](https://github.com/oskarsh/Yin-Yang/wiki/Contributing)].

[![](https://opencollective.com/Yin-Yang/contributors.svg?button=false)](https://github.com/oskarsh/Yin-Yang/graphs/contributors)

### Donate

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
