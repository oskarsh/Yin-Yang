#!/bin/bash

set -euo pipefail

USER_HOME=${1-${HOME}}

if test ${EUID} -ne 0; then
    echo enter password in order to install Yin-Yang correctly
    exec sudo su -c "${0} ${USER_HOME}"
    exit 0
fi

echo "Uninstalling old version, if it exists"
./scripts/uninstall.sh

echo "Installing dependencies …"
# Tell Poetry not to use a keyring
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
# create virtual environment and install packages
poetry env use python
poetry install --sync
poetry build
pip install ./dist/yin_yang-*-py3-none-any.whl

echo "Installing yin yang"
#check if /opt/ directory exists else create
if [ ! -d /opt/ ]; then
    mkdir -p /opt/
fi
#check if /opt/ directory exists else create
if [ ! -d /opt/yin_yang/ ]; then
    mkdir -p /opt/yin_yang/
fi
# check directories for extension
if [ ! -d /usr/lib/mozilla ]; then
    mkdir -p /usr/lib/mozilla
fi
if [ ! -d /usr/lib/mozilla/native-messaging-hosts/ ]; then
    mkdir -p /usr/lib/mozilla/native-messaging-hosts/
fi
if [ ! -d "$USER_HOME/.local/share/applications/" ]; then
    mkdir -p "$USER_HOME/.local/share/applications/"
fi
# copy files TODO this copies a bunch of unnecessary files
cp -r ./* /opt/yin_yang/
# copy manifest for firefox extension
cp ./resources/yin_yang.json /usr/lib/mozilla/native-messaging-hosts/
# copy terminal executive
cp ./resources/yin_yang /usr/bin/
# copy .desktop file
appstreamcli make-desktop-file "$USER_HOME/.local/share/applications/yin_yang.desktop"
# copy icon
cp ./resources/icon.svg /usr/share/icons/hicolor/scalable/apps/sh.oskar.yin_yang.svg
# systemd unit files will be installed by the app

cat << "EOF"
 __     ___          __     __
 \ \   / (_)         \ \   / /
  \ \_/ / _ _ __ _____\ \_/ /_ _ _ __   __ _
   \   / | | '_ \______\   / _` | '_ \ / _` |
    | |  | | | | |      | | (_| | | | | (_| |
    |_|  |_|_| |_|      |_|\__,_|_| |_|\__, |
                                        __/ |
                                       |___/
EOF
echo ""
echo "Yin & Yang brings Auto Night mode for Linux"
echo ""
cat << "EOF"
       _..oo8"""Y8b.._
     .88888888o.    "Yb.
   .d888P""Y8888b      "b.
  o88888    88888)       "b
 d888888b..d8888P         'b
 88888888888888"           8
(88DWB8888888P             8)
 8888888888P               8
 Y88888888P     ee        .P
  Y888888(     8888      oP
   "Y88888b     ""     oP"
     "Y8888o._     _.oP"
       `""Y888boodP""'

EOF
echo ""
echo ""
echo "checkout https://github.com/daehruoydeef/Yin-Yang for help"
echo "Yin & Yang is now installed"
echo "Please make sure you have systemd and python-systemd installed on your system via your package manager!"
