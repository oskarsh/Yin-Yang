#!/bin/#!/bin/sh

# this script will uninstall Yin-Yang and will also delete its config files

if [ "$EUID" -ne 0 ]; then
    echo enter password in order to uninstall Yin-Yang correctly
    sudo sh ./$0
    exit 1
fi

rm -rf /opt/yin-yang /usr/bin/yin-yang/ ~/.config/yin-yang/ 
rm -rf ~/.local/share/applications/Yin-Yang.desktop


echo Yin-Yang uninstalled succesfully
echo have a nice day ...
