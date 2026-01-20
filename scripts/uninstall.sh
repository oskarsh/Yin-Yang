#!/bin/bash

# this script will uninstall Yin & Yang and will also delete its config files

set -euo pipefail

flatpak_uninstall() {
    if command -v flatpak > /dev/null ; then
        flatpak uninstall "$1" --noninteractive --delete-data sh.oskar.yin_yang \
        || echo Already uninstalled from flatpak "$1"
    fi
}

flatpak_uninstall --user

# check, if sudo
if test ${EUID} -ne 0; then
    echo "enter password in order to install Yin & Yang correctly"
    exec sudo su -c "${0} ${HOME}"
    exit 0
fi

echo "Removing config and .desktop file"
rm -f "$HOME/.local/share/applications/yin_yang.desktop"
rm -f "$HOME/.local/share/yin_yang.log"
rm -f "/usr/share/icons/hicolor/scalable/apps/yin_yang.svg"
# rm -rf "$HOME/.config/yin_yang"

echo "Removing program and terminal execution"
rm -rf /opt/yin_yang /usr/bin/yin_yang

echo "Removing manifest"
rm -f /usr/lib/mozilla/native-messaging-hosts/yin_yang.json

echo "Removing systemd units"
rm -f "$HOME/.local/share/systemd/user/yin_yang.timer"
rm -f "$HOME/.local/share/systemd/user/yin_yang.service"

flatpak_uninstall --system

echo "Yin & Yang uninstalled succesfully"
echo have a nice day ...
