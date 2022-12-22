# ![Yin & Yang logo](resources/logo.svg) Yin-Yang


Auto Night-mode for Linux, it supports popular Desktops like KDE, Gnome, Budgie 
and also themes your favourite editors like VSCode or Atom.

> Translations: [🇨🇳](README_zh.md)

![](https://img.shields.io/github/v/release/oskarsh/yin-yang)
![](https://img.shields.io/github/v/release/oskarsh/yin-yang?include_prereleases)
![](https://img.shields.io/github/downloads/oskarsh/yin-yang/total)
![](https://img.shields.io/badge/Build%20with-Python-yellow)
![](https://img.shields.io/github/license/oskarsh/yin-yang)

![](.github/images/header.png)

## Features

![](.github/images/settings.png)

* Changes your themes at certain times or sunrise and sunset
* Supported Desktops:
  * Gnome
  * Budgie
  * KDE Plasma
* Supported applications:
  * VSCode
  * Atom
* Miscellaneous:
  * Wallpaper change
  * Notifications on theme change
  * Play a sound

> To see planned features and the development status, visit the [project status page](https://github.com/oskarsh/Yin-Yang/projects?type=classic).

## Installation

### Dependencies:
Yin-Yang depends on `python-systemd` and `pyside6` from pypi. `python-systemd` requires you have installed the systemd-headers from your package manager.

For CentOS, RHEL, and Fedora:
```bash
sudo dnf install gcc systemd-devel
``` 

For Debian, Ubuntu, etc.
```bash
sudo apt update
sudo apt install libsystemd-dev gcc
```

### Yin-Yang
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
