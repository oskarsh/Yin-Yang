#!/bin/bash

# this script will uninstall Yin-Yang and will also delete its config files

set -euo pipefail

# check, if sudo
if test ${EUID} -ne 0; then
    echo enter password in order to install Yin-Yang correctly
    exec sudo su -c "${0} ${HOME}"
    exit 0
fi

echo "Removing config and .desktop file"
rm -f "$HOME/.local/share/applications/Yin-Yang.desktop"
rm -f "$HOME/.local/share/yin_yang.log"
rm -f "/usr/share/icons/hicolor/scalable/apps/yin_yang.svg"
rm -rf "$HOME/.config/yin_yang"

echo "Removing program and terminal execution"
rm -rf /opt/yin-yang /usr/bin/yin-yang

echo "Removing manifest"
rm -f /usr/lib/mozilla/native-messaging-hosts/yin_yang.json

echo Yin-Yang uninstalled succesfully
echo have a nice day ...
