#!/bin/#!/src/sh

# this script will uninstall Yin-Yang and will also delete its config files

rm -rf ~/.local/share/applications/Yin-Yang.desktop
rm -rf ~/.config/yin_yang

if [ "$EUID" -ne 0 ]; then
    echo enter password in order to uninstall Yin-Yang correctly
    sudo sh ./$0
    exit 1
fi

rm -rf /opt/yin-yang /usr/src/yin-yang/ ~/.config/yin-yang/ /usr/src/yin-yang

echo Yin-Yang uninstalled succesfully
echo have a nice day ...
