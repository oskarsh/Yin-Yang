#!/bin/bash

# resource file
pyside6-rcc ./resources/resources.qrc -o ./yin_yang/ui/resources_rc.py
# ui file from qt designer
pyside6-uic --from-imports ./designer/main_window.ui -o ./yin_yang/ui/main_window.py
# extract strings to translate (doesn't work with .pro file unfortunately)
pyside6-lupdate ./designer/main_window.ui ./yin_yang/* \
  -ts resources/translations/yin_yang.*.ts -no-obsolete
# generate binary translation files
pyside6-lrelease ./resources/translations/yin_yang.*.ts
