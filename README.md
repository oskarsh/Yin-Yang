# Yin-Yang KDE ![icon](/home/daeh/Git/Yin-Yang/bin/ui/assets/icon.png)

Yin & Yang is a KDE tool which brings Auto Night-mode for KDE, VSCode and all GTK Apps like Firefox, Libreoffice and Chromium. On Top of that it let´s you specify Wallpaper swhich will be toggled alongisde. Yin & Yang styles all KDE and QT5 tools, furthermore it also themes VSCode or VSCodium. You can activate a Theme-toggle with shortcuts or let Yin-Yang toggle themes at scheduled Times.

# ![yin_yang_demo](/home/daeh/Git/Yin-Yang/assets/yin_yang_demo.png)



## TODO INSERT GIF



## Installation

```bash
$ git clone git@github.com:daehruoydeef/Yin-Yang.git
$ cd Yin-Yang
# NOTE: the install script will ask you for sudo permission
$ sh install.sh
```

Note: You should use yin-yang on the first run with it´s GUI and configure the Settings to your likings. This way it will configure itself correctly and can be used after this inital step as a standalone terminal applicaton or to your liking with a modern QT5 Gui.



## Hotkeys

Yin-Yang is about flexibility and stability, it does not provide basic shortcuts for **Dark/Light theme** toggle. It is recommended to add **Hotkeys with the KDE Hotkeys Module** found inside the **System preferences** under the **Hotkeys** section. Set any Hotkey you want to run the command:

```bash
# Toggle between Light & Dark theme, good for settings as a shortcut
$ yin-yang
```

```bash
# opens the QT5 Gui and allows for further customization
$ yin-yang -Gui
```

```bash
# lets you activate the sheduler, good if you want to autostart yin-yang on startup
$ yin-yang -s
```



## Updates

Yin-Yang was designed to be updated by the install.sh script which will simply replace the existing Yin-Yang installation. If you plan on updating there is currently no "auto update" and it is recommended to **star** or **watch** this repository and reclone it if a new version is released.

You can update Yin-Yang by simply clone this repository and run the install again, it will update everything and you should be good to go.



## Why I created Yin & Yang KDE

I found myself constantly switching between themes to match my surrounding lights. I prefer a Dark theme in the Night while I want good readability at Day time. I want to easily switch my whole enviroment to a dark / light theme based on a pre defined time. I wanted to provide this as open software so everyone can benefit and I hope that I inspire other talented developers to also start a open source Project and better the Linux Desktop. This is why I created Yin-Yang.

> The best way to find yourself is to lose yourself in the service of others. 
>
> Gandhi

## Requirements

If you do not got **qtpy** or **pyqt5** installed, Yin-Yang got your back by installing the necessary requirements on the go with pip3.

- pip3 \*
- python3 \*
- qtpy
- pyqt5

## FAQ

## Contributions

If you are interested in making this project better or just want to support me (the developer), I compiled a list of various methods on how you can Contribute even without Coding skills.

### Code contributing



### Bug hunting

### Create Yin-Yang wallpapers



## Troubleshooting

Please try to answer the following Questions, if you still not solved the Problem please write a GitHub Issue

### I cannot install yin-yang

> Did you ran 
>
> $ sh install.sh
>
>  and provided your password as asked?

### First run, does not start

> Do you have all the requirements installed mainly
>
> * python3
> * pyqt5
> * qtpy

> Did you try to run the first time in console without Gui?

> Is the config and path created correctly?
>
> check ~/.config/yin_yang/yin_yang.json

### KDE is not working

### VSCode is not working

### GTK is not working

> Did you ever changed the GTK Settings

> Is the theme name correctly written

### Wallpaper is not working

> Did you specified the correct images with .jpg or .png extension

> is the 
>
> $ dbus-send 
>
> command working?

