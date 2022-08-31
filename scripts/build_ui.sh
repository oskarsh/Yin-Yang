#!/bin/bash

# resource file
pyside6-rcc ./resources/resources.qrc -o ./resources_rc.py
# ui file from qt designer
pyside6-uic ./designer/main_window.ui > ./src/ui/main_window.py
# extract strings to translate (doesn't work with .pro file unfortunately)
pyside6-lupdate ./designer/main_window.ui ./src/ui/config_window.py \
  -ts resources/translations/yin_yang.de_DE.ts -no-obsolete
# generate binary translation files
pyside6-lrelease ./resources/translations/yin_yang.de_DE.ts
