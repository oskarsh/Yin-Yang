#!/bin/sh
if [ "$EUID" -ne 0 ]; then
    echo enter password in order to install Yin-Yang correctly
    sudo sh ./$0
    exit 1
fi
echo "Installing Yin-Yang ..."
echo ""
echo "Checking for QT dependencies"
echo ""
#checking python dependencies
pip3 install qtpy
pip3 install pyqt5
echo ""
echo "Checking and creating correct folders ..."
#check if /opt/ directory exists else create
if [ ! -d /opt/ ]; then
    mkdir /opt/
fi
#check if /opt/ directory exists else create
if [ ! -d /opt/yin-yang/ ]; then
    mkdir /opt/yin-yang/
fi
echo ""
echo "done"
echo ""
echo "Installin yin-yang for Commandline usage"
# copy files
cp -r ./* /opt/yin-yang/
#copy terminal executive
cp ./src/yin-yang /usr/src/
sudo chmod +x /usr/src/yin-yang
echo "Creating .desktop file for native enviroment execution"
#create .desktop file
cat <<EOF >/home/$SUDO_USER/.local/share/applications/Yin-Yang.desktop
[Desktop Entry]
# The type as listed above
Type=Application
# The version of the desktop entry specification to which this file complies
Version=0.0.1
# The name of the application
Name=Yin & Yang
# A comment which can/will be used as a tooltip
Comment=Auto Nightmode for KDE and VSCode
# The path to the folder in which the executable is run
Path=/opt/yin-yang
# The executable of the application, possibly with arguments.
Exec=sh yin-yang "-gui"
# The name of the icon that will be used to display this entry
Icon=/opt/yin-yang/src/ui/assets/icon.png
# Describes whether this application needs to be run in a terminal or not
Terminal=false
# Describes the categories in which this entry should be shown
Categories=Education;Languages;Python; Cool;
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
