#!/bin/bash

set -euo pipefail

YIN_YANG_HOME=${1-${HOME}}

if test ${EUID} -ne 0; then
    echo enter password in order to install Yin-Yang correctly
    exec sudo su -c "${0} ${HOME}"
    exit 0
fi

echo "removing old Yin-Yang files if they exist"
echo "your home here is" ${YIN_YANG_HOME}
./uninstall.sh ${YIN_YANG_HOME}

echo "Installing Yin-Yang ..."
echo ""
echo "Checking for QT dependencies"
echo ""
#checking python dependencies
pip3 install qtpy
pip3 install pyqt5
pip3 install suntime
echo ""
echo "Checking and creating correct folders ..."
#check if /opt/ directory exists else create
if [ ! -d /opt/ ]; then
    mkdir -p /opt/
fi
#check if /opt/ directory exists else create
if [ ! -d /opt/yin-yang/ ]; then
    mkdir -p /opt/yin-yang/
fi
# check directories for extension
if [ ! -d /usr/lib/mozilla ]; then
    mkdir -p /usr/lib/mozilla
fi
if [ ! -d /usr/lib/mozilla/native-messaging-hosts/ ]; then
    mkdir -p /usr/lib/mozilla/native-messaging-hosts/
fi
if [ ! -d "${YIN_YANG_HOME}/.local/share/applications/" ]; then
    mkdir -p "${YIN_YANG_HOME}/.local/share/applications/"
fi
echo ""
echo "done"
echo ""
echo "Installin yin-yang for Commandline usage"
# copy files
cp -r ./* /opt/yin-yang/
# copy manifest for firefox extension
cp ./assets/yin_yang.json /usr/lib/mozilla/native-messaging-hosts/
#copy terminal executive
cp ./src/yin-yang /usr/bin/
chmod +x /usr/bin/yin-yang
echo "Creating .desktop file for native enviroment execution"
#create .desktop file
cat > "${YIN_YANG_HOME}/.local/share/applications/Yin-Yang.desktop" <<EOF
[Desktop Entry]
# The type as listed above
Type=Application
# The version of the desktop entry specification to which this file complies
Version=1.4
# The name of the application
Name=Yin & Yang
# Generic name of the application, for example "Web Browser"
GenericName=Theme Switcher
# A comment which can/will be used as a tooltip
Comment=Auto Nightmode for KDE and VSCode
# The path to the folder in which the executable is run
Path=/opt/yin-yang
# The executable of the application, possibly with arguments.
Exec=env QT_AUTO_SCREEN_SCALE_FACTOR=1 sh /usr/bin/yin-yang
# The name of the icon that will be used to display this entry
Icon=/opt/yin-yang/src/ui/assets/yin-yang.svg
# Describes whether this application needs to be run in a terminal or not
Terminal=false
# Describes the categories in which this entry should be shown
Categories=Utility; System; Settings;
# A list of strings which may be used in addition to other metadata to describe this entry
Keywords=night;dark;day;bright;color;theme;
EOF

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
echo "Yin-Yang brings Auto Nightmode for KDE and VSCode"
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
echo "Yin-Yang is now installed"
