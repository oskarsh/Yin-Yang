#!/bin/bash
#
# this script will convert the project Yin-Yang to a executable .deb and more importantly an AppImage
# first it converts the main.py to an executable binary -> then it builds the .deb packages, it creates the folder structure


# create binary
 python3 -m PyInstaller --onefile main.spec


# create folder strcuture for a debian package
# it should look like this:
# ├── DEBIAN
# │   └── control
# └── usr
#     ├── bin
#     │   └── yin-yang
#     ├── icons
#     │   └── hicolor
#     │       └── scalable
#     │           └── apps
#     │               └── icon.png
#     └── share
#         └── applications
#             └── yin-yang.desktop
mkdir -p dist/yin-yang-build/yin-yang_3.0/DEBIAN/
mkdir -p dist/yin-yang-build/yin-yang_3.0/usr/bin/
mkdir -p dist/yin-yang-build/yin-yang_3.0/usr/icons/hicolor/scalable/apps/
mkdir -p dist/yin-yang-build/yin-yang_3.0/usr/share/applications/


# copy all the necassary files like the binary, icon.png, yin-yang.deskop, CONTROL
cp build/yin-yang.desktop dist/yin-yang-build/yin-yang_3.0/usr/share/applications/yin-yang.desktop
cp build/control dist/yin-yang-build/yin-yang_3.0/DEBIAN/control
cp assets/icon.png dist/yin-yang-build/yin-yang_3.0/usr/icons/hicolor/scalable/apps/icon.png
cp build/yin-yang.yml dist/yin-yang-build/yin-yang.yml

# create the .deb package
dpkg-deb --build dist/yin-yang-build/yin-yang_3.0

cd build

# create the AppImage out of the deb package
bash -ex ./pkg2app.sh ../dist/yin-yang-build/yin-yang.yml
