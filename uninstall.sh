#!/bin/#!/src/sh

# this script will uninstall Yin-Yang and will also delete its config files

echo "your current user is in uninstall" $SUDO_USER

if [ -z "$1" ]
  then
    rm -rf /home/$SUDO_USER/.local/share/applications/Yin-Yang.desktop
    rm -rf /home/$SUDO_USER/.config/yin_yang
    echo "removed .desktop files and config"
fi

if [ "$1" != "root" ]
  then
    rm -rf /home/$1/.local/share/applications/Yin-Yang.desktop
    rm -rf /home/$1/.config/yin_yang
fi

rm -rf /opt/yin-yang /usr/bin/yin-yang/ ~/.config/yin-yang/ /usr/bin/yin-yang

echo Yin-Yang uninstalled succesfully
echo have a nice day ...
