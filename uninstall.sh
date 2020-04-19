#!/bin/sh

# this script will uninstall Yin-Yang and will also delete its config files

# check, if sudo
if [ "$EUID" -ne 0 ]; then
    echo enter password in order to install Yin-Yang correctly
    sudo sh $0
    exit 1
fi

echo "your current user is in uninstall" $SUDO_USER

echo "Removing config and .desktop file"
rm -rf /home/$SUDO_USER/.local/share/applications/Yin-Yang.desktop
rm -rf /home/$SUDO_USER/.config/yin_yang

echo "Removing program and terminal execution"
rm -rf /opt/yin-yang /usr/bin/yin-yang

echo "Removing manifest"
rm -f /usr/lib/mozilla/native-messaging-hosts/yin_yang.json

echo Yin-Yang uninstalled succesfully
echo have a nice day ...
