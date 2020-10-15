# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsOqOqhJ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc

class Ui_PluginWindow(object):
    def setupUi(self, PluginWindow):
        if not PluginWindow.objectName():
            PluginWindow.setObjectName(u"PluginWindow")
        PluginWindow.setEnabled(True)
        PluginWindow.resize(357, 495)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PluginWindow.sizePolicy().hasHeightForWidth())
        PluginWindow.setSizePolicy(sizePolicy)
        PluginWindow.setMinimumSize(QSize(357, 495))
        PluginWindow.setMaximumSize(QSize(1000, 1000))
        PluginWindow.setBaseSize(QSize(260, 300))
        icon = QIcon()
        icon.addFile(u":/icons/assets/yin-yang.svg", QSize(), QIcon.Normal, QIcon.Off)
        PluginWindow.setWindowIcon(icon)
        self.centralWidget = QWidget(PluginWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.header = QHBoxLayout()
        self.header.setSpacing(6)
        self.header.setObjectName(u"header")
        self.labelHeader = QLabel(self.centralWidget)
        self.labelHeader.setObjectName(u"labelHeader")
        self.labelHeader.setMaximumSize(QSize(16777215, 50))
        self.labelHeader.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelHeader.setFont(font)

        self.header.addWidget(self.labelHeader)

        self.buttonBack = QPushButton(self.centralWidget)
        self.buttonBack.setObjectName(u"buttonBack")

        self.header.addWidget(self.buttonBack, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_3.addLayout(self.header)

        self.tabWidget = QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabSystem = QWidget()
        self.tabSystem.setObjectName(u"tabSystem")
        self.verticalLayout_2 = QVBoxLayout(self.tabSystem)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupKde = QGroupBox(self.tabSystem)
        self.groupKde.setObjectName(u"groupKde")
        self.groupKde.setCheckable(True)
        self.horizontalLayout_9 = QHBoxLayout(self.groupKde)
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.kde_combo_light = QComboBox(self.groupKde)
        self.kde_combo_light.setObjectName(u"kde_combo_light")

        self.horizontalLayout_9.addWidget(self.kde_combo_light)

        self.kde_combo_dark = QComboBox(self.groupKde)
        self.kde_combo_dark.setObjectName(u"kde_combo_dark")

        self.horizontalLayout_9.addWidget(self.kde_combo_dark)


        self.verticalLayout_2.addWidget(self.groupKde)

        self.groupGnome = QGroupBox(self.tabSystem)
        self.groupGnome.setObjectName(u"groupGnome")
        self.groupGnome.setCheckable(True)
        self.horizontalLayout_2 = QHBoxLayout(self.groupGnome)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gnome_lineEdit_dark = QLineEdit(self.groupGnome)
        self.gnome_lineEdit_dark.setObjectName(u"gnome_lineEdit_dark")

        self.horizontalLayout_2.addWidget(self.gnome_lineEdit_dark)

        self.gnome_lineEdit_light = QLineEdit(self.groupGnome)
        self.gnome_lineEdit_light.setObjectName(u"gnome_lineEdit_light")

        self.horizontalLayout_2.addWidget(self.gnome_lineEdit_light)


        self.verticalLayout_2.addWidget(self.groupGnome)

        self.groupGtk = QGroupBox(self.tabSystem)
        self.groupGtk.setObjectName(u"groupGtk")
        self.groupGtk.setCheckable(True)
        self.groupGtk.setChecked(True)
        self.horizontalLayout_5 = QHBoxLayout(self.groupGtk)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.gtk_line_light = QLineEdit(self.groupGtk)
        self.gtk_line_light.setObjectName(u"gtk_line_light")

        self.horizontalLayout_5.addWidget(self.gtk_line_light)

        self.gtk_line_dark = QLineEdit(self.groupGtk)
        self.gtk_line_dark.setObjectName(u"gtk_line_dark")

        self.horizontalLayout_5.addWidget(self.gtk_line_dark)


        self.verticalLayout_2.addWidget(self.groupGtk)

        self.groupWallpaper = QGroupBox(self.tabSystem)
        self.groupWallpaper.setObjectName(u"groupWallpaper")
        self.groupWallpaper.setCheckable(True)
        self.horizontalLayout_7 = QHBoxLayout(self.groupWallpaper)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.wallpaper_button_light = QPushButton(self.groupWallpaper)
        self.wallpaper_button_light.setObjectName(u"wallpaper_button_light")

        self.horizontalLayout_7.addWidget(self.wallpaper_button_light)

        self.wallpaper_button_dark = QPushButton(self.groupWallpaper)
        self.wallpaper_button_dark.setObjectName(u"wallpaper_button_dark")

        self.horizontalLayout_7.addWidget(self.wallpaper_button_dark)


        self.verticalLayout_2.addWidget(self.groupWallpaper)

        self.tabWidget.addTab(self.tabSystem, "")
        self.tabApplications = QWidget()
        self.tabApplications.setObjectName(u"tabApplications")
        self.verticalLayout_4 = QVBoxLayout(self.tabApplications)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupFirefox = QGroupBox(self.tabApplications)
        self.groupFirefox.setObjectName(u"groupFirefox")
        self.groupFirefox.setCheckable(True)
        self.horizontalLayout_3 = QHBoxLayout(self.groupFirefox)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.firefox_line_light = QLineEdit(self.groupFirefox)
        self.firefox_line_light.setObjectName(u"firefox_line_light")

        self.horizontalLayout_3.addWidget(self.firefox_line_light)

        self.firefox_line_dark = QLineEdit(self.groupFirefox)
        self.firefox_line_dark.setObjectName(u"firefox_line_dark")

        self.horizontalLayout_3.addWidget(self.firefox_line_dark)


        self.verticalLayout_4.addWidget(self.groupFirefox)

        self.groupVscode = QGroupBox(self.tabApplications)
        self.groupVscode.setObjectName(u"groupVscode")
        self.groupVscode.setCheckable(True)
        self.horizontalLayout = QHBoxLayout(self.groupVscode)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.code_line_light = QLineEdit(self.groupVscode)
        self.code_line_light.setObjectName(u"code_line_light")

        self.horizontalLayout.addWidget(self.code_line_light)

        self.code_line_dark = QLineEdit(self.groupVscode)
        self.code_line_dark.setObjectName(u"code_line_dark")

        self.horizontalLayout.addWidget(self.code_line_dark)


        self.verticalLayout_4.addWidget(self.groupVscode)

        self.groupAtom = QGroupBox(self.tabApplications)
        self.groupAtom.setObjectName(u"groupAtom")
        self.groupAtom.setCheckable(True)
        self.horizontalLayout_8 = QHBoxLayout(self.groupAtom)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.atom_line_light = QLineEdit(self.groupAtom)
        self.atom_line_light.setObjectName(u"atom_line_light")

        self.horizontalLayout_8.addWidget(self.atom_line_light)

        self.atom_line_dark = QLineEdit(self.groupAtom)
        self.atom_line_dark.setObjectName(u"atom_line_dark")

        self.horizontalLayout_8.addWidget(self.atom_line_dark)


        self.verticalLayout_4.addWidget(self.groupAtom)

        self.tabWidget.addTab(self.tabApplications, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        PluginWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QStatusBar(PluginWindow)
        self.statusBar.setObjectName(u"statusBar")
        PluginWindow.setStatusBar(self.statusBar)

        self.retranslateUi(PluginWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PluginWindow)
    # setupUi

    def retranslateUi(self, PluginWindow):
        PluginWindow.setWindowTitle(QCoreApplication.translate("PluginWindow", u"Yin & Yang", None))
        self.labelHeader.setText(QCoreApplication.translate("PluginWindow", u"Settings", None))
        self.buttonBack.setText(QCoreApplication.translate("PluginWindow", u"back", None))
        self.groupKde.setTitle(QCoreApplication.translate("PluginWindow", u"KDE", None))
        self.groupGnome.setTitle(QCoreApplication.translate("PluginWindow", u"Gnome", None))
        self.gnome_lineEdit_dark.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Light Theme", None))
        self.gnome_lineEdit_light.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Dark Theme", None))
        self.groupGtk.setTitle(QCoreApplication.translate("PluginWindow", u"GTK", None))
        self.gtk_line_light.setText("")
        self.gtk_line_light.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Light Theme", None))
        self.gtk_line_dark.setText("")
        self.gtk_line_dark.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Dark Theme", None))
        self.groupWallpaper.setTitle(QCoreApplication.translate("PluginWindow", u"Wallpaper", None))
        self.wallpaper_button_light.setText(QCoreApplication.translate("PluginWindow", u"open light wallpaper", None))
        self.wallpaper_button_dark.setText(QCoreApplication.translate("PluginWindow", u"open dark wallpaper", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSystem), QCoreApplication.translate("PluginWindow", u"System", None))
        self.groupFirefox.setTitle(QCoreApplication.translate("PluginWindow", u"Firefox", None))
        self.firefox_line_light.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Light Theme", None))
        self.firefox_line_dark.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Dark Theme", None))
        self.groupVscode.setTitle(QCoreApplication.translate("PluginWindow", u"VS Code", None))
        self.code_line_light.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Light Theme", None))
        self.code_line_dark.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Dark Theme", None))
        self.groupAtom.setTitle(QCoreApplication.translate("PluginWindow", u"Atom", None))
        self.atom_line_light.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Light Theme", None))
        self.atom_line_dark.setPlaceholderText(QCoreApplication.translate("PluginWindow", u"Dark Theme", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabApplications), QCoreApplication.translate("PluginWindow", u"Applications", None))
    # retranslateUi

