# Yin-Yang KDE ![icon](./src/ui/assets/icon.png)

Yin & Yang is a KDE tool which brings Auto Night-mode for KDE, VSCode and all GTK Apps like Firefox, Libreoffice and Chromium. On Top of that it let´s you specify Wallpaper swhich will be toggled alongisde. Yin & Yang styles all KDE and QT5 tools, furthermore it also themes VSCode or VSCodium. You can activate a Theme-toggle with shortcuts or let Yin-Yang toggle themes at scheduled Times.

# ![yin_yang_demo](./assets/yin-yang.gif)



## Installation

```bash
$ git clone https://github.com/daehruoydeef/Yin-Yang.git
$ cd Yin-Yang
# the -H flag will install a .desktop file in your home directory
$ sudo sh install.sh
```

**Note:** You should use yin-yang on the first run with it´s GUI and configure the Settings to your likings. This way it will configure itself correctly and can be used after this inital step as a standalone terminal Applicaton or as usual with the GUI



## Uninstall

```bash
$ cd Yin-yang
$ sudo sh uninstall.sh

```



## Updates

Yin-Yang was designed to be updated by the install.sh script which will simply replace the existing Yin-Yang installation. If you plan on updating there is currently no "auto update" and it is recommended to **star** or **watch** this repository and reclone it if a new version is released.

You can update Yin-Yang by simply clone this repository and run the install again, it will update everything and you should be good to go.

**Note:** **When you Update Yin-Yang the config get's deleted**. This allows us to easily add programs and ensure that the config is always fresh and included all the necessary Fields for the new programs. This it is how it is right now, we would like to switch to Delta updates as soon as possible but apparently it is not doable right now.

That means that you need to open Yin-Yang with it's GUI and set all the Themes again.

You can use the System settings and add Yin-Yang to autostart via the KDE autostart manager.



## Hotkeys

Yin-Yang is about flexibility and stability, it does not provide basic shortcuts for **Dark/Light theme** toggle. It is recommended to add **Hotkeys with the KDE Hotkeys Module** found inside the **System preferences** under the **Hotkeys** section. Set any Hotkey you want to run the command:

```bash
# Toggle between Light & Dark theme, good for settings as a shortcut
$ yin-yang
```

```bash
# opens the QT5 Gui and allows for further customization
$ yin-yang -gui
```

```bash
# lets you activate the sheduler, good if you want to autostart yin-yang on startup
$ yin-yang -s
```



## Wallpapers

Yin-Yang comes with custom made Wallpaper in order to get you started with Light / Dark Wallpapers, you can check out the repository here

[Wallpaper Yin-Yang](https://github.com/daehruoydeef/Wallpaper-yin-yang)

The Wallpapers are open source and can be used however you want. I also accept contributions in form of open source Wallpapers see the Contribution Section.



## Why I created Yin & Yang KDE

I found myself constantly switching between themes to match my surrounding lights. I prefer a Dark theme at Night while I want good readability at Day time. I want to easily switch my whole enviroment to a dark / light theme based on a pre defined time. I wanted to provide this as open software so everyone can benefit and I hope that I inspire other talented developers to also start a open source Project and better the Linux Desktop. This is why I created Yin-Yang.



## Requirements

If you do not got **qtpy** or **pyqt5** installed, Yin-Yang got your back by installing the necessary requirements on the go with pip3.

- pip3 \*
- python3 \*
- qtpy
- pyqt5



## Contributions

### Bug hunting

Try finding bugs and report them, eventually I will fix them and everyone benefits. You should use the GitHub Issues site to report them

### Create Yin-Yang wallpapers

If you are not into coding but into Design I much appreciate Wallpapers featuring a Light theme and a Dark theme. The Wallpapers must be under a free open source License. You can use [Firefox Send](https://send.firefox.com/) to send the Wallpapers as a Zip. I will include them inside a extra Repository which can be found [here](https://github.com/daehruoydeef/Wallpaper-yin-yang)

## Troubleshooting

Please try to answer the following Questions, if you still not solved the Problem please write a GitHub Issue

### I cannot install yin-yang

You can check if Yin-Yang installed correctly by searching yin-yang -gui into the terminal.

Yin-Yang installs itself at following locations

* /usr/bin/yin-yang

* /opt/bin/yin-yang

* ~/.config/yin_yang/yin_yang.json

~/.local/share/applications/Yin-Yang.desktop



if some of these files are missing please file a bug report.



### First run, does not start

Do you have all the requirements installed mainl

* python3
* pyqt
* qtpy5

Did you try to run the first time in console without Gui?

Is the config and path created correctly? check ~/.config/yin_yang/yin_yang.json



### My Desktop Environment is not working

check the .json file under

~/.config/yin_yang/yin_yang.json

if "desktop"="undefined" please replace "undefined" with either "kde" or "gtk"



## How do I disable the Sound?

simply delete the sound files found in /opt/yin-yang/assets/*.wav



### VSCode is not working

There is a Bug in VSCode that on the first start without ever touching any settings there will none be created! Yin-Yang can not help. You can fix this by simply going into VSCode and set a theme manually. Afterwards yin-yang should work.



## Atom is not working

Try to change your theme manually then let Yin-Yang try, sometimes there must be settings created before Yin-Yang can get to work. 

If this is not working please file a bug report.



### GTK3 is not working (KDE only)

Basically the same as with VSCode, you need to manually set a GTK Theme first in order for the settings to be created. Yin-Yang will do the rest.

Did you wrote the Theme name correctly, you can check available themes under **Systemsettings › Application-Style › GNOME Application-Style(GTK) › Choose a GTK3-Design**. Inside the Dropdown menu you can see which themes are available. Only GTK3 themes are supported



### Wallpaper is not working

Did you specified the correct images with .jpg or .png extension

