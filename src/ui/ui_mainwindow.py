# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowreyxAQ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(261, 515)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(261, 515))
        MainWindow.setMaximumSize(QSize(300, 600))
        MainWindow.setBaseSize(QSize(300, 460))
        icon = QIcon()
        icon.addFile(u":/icons/assets/yin-yang.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.logo = QHBoxLayout()
        self.logo.setSpacing(6)
        self.logo.setObjectName(u"logo")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.logo.addItem(self.horizontalSpacer)

        self.imgLogo = QLabel(self.centralWidget)
        self.imgLogo.setObjectName(u"imgLogo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.imgLogo.sizePolicy().hasHeightForWidth())
        self.imgLogo.setSizePolicy(sizePolicy1)
        self.imgLogo.setMinimumSize(QSize(0, 0))
        self.imgLogo.setMaximumSize(QSize(1000, 1000))
        self.imgLogo.setSizeIncrement(QSize(0, 0))
        self.imgLogo.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(20)
        self.imgLogo.setFont(font)
        self.imgLogo.setTextFormat(Qt.RichText)
        self.imgLogo.setPixmap(QPixmap(u":/icons/assets/yin-yang.svg"))
        self.imgLogo.setScaledContents(True)
        self.imgLogo.setAlignment(Qt.AlignCenter)

        self.logo.addWidget(self.imgLogo)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.logo.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.logo)

        self.manual = QWidget(self.centralWidget)
        self.manual.setObjectName(u"manual")
        self.manual.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.manual.sizePolicy().hasHeightForWidth())
        self.manual.setSizePolicy(sizePolicy2)
        self.horizontalLayout = QHBoxLayout(self.manual)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonLight = QPushButton(self.manual)
        self.buttonLight.setObjectName(u"buttonLight")
        self.buttonLight.setAutoDefault(False)
        self.buttonLight.setFlat(False)

        self.horizontalLayout.addWidget(self.buttonLight)

        self.buttonDark = QPushButton(self.manual)
        self.buttonDark.setObjectName(u"buttonDark")

        self.horizontalLayout.addWidget(self.buttonDark)


        self.verticalLayout_2.addWidget(self.manual)

        self.automatic = QGroupBox(self.centralWidget)
        self.automatic.setObjectName(u"automatic")
        self.automatic.setCheckable(True)
        self.automatic.setChecked(True)
        self.verticalLayout = QVBoxLayout(self.automatic)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.buttonSchedule = QRadioButton(self.automatic)
        self.buttonSchedule.setObjectName(u"buttonSchedule")

        self.verticalLayout.addWidget(self.buttonSchedule)

        self.time = QFrame(self.automatic)
        self.time.setObjectName(u"time")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.time.sizePolicy().hasHeightForWidth())
        self.time.setSizePolicy(sizePolicy3)
        self.formLayout = QFormLayout(self.time)
        self.formLayout.setSpacing(6)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignCenter)
        self.formLayout.setHorizontalSpacing(40)
        self.labelLight = QLabel(self.time)
        self.labelLight.setObjectName(u"labelLight")
        self.labelLight.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelLight)

        self.inTimeLight = QTimeEdit(self.time)
        self.inTimeLight.setObjectName(u"inTimeLight")
        self.inTimeLight.setTime(QTime(8, 0, 0))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.inTimeLight)

        self.labelDark = QLabel(self.time)
        self.labelDark.setObjectName(u"labelDark")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelDark)

        self.inTimeDark = QTimeEdit(self.time)
        self.inTimeDark.setObjectName(u"inTimeDark")
        self.inTimeDark.setTime(QTime(20, 0, 0))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.inTimeDark)


        self.verticalLayout.addWidget(self.time)

        self.buttonSun = QRadioButton(self.automatic)
        self.buttonSun.setObjectName(u"buttonSun")

        self.verticalLayout.addWidget(self.buttonSun)

        self.location = QFrame(self.automatic)
        self.location.setObjectName(u"location")
        self.location.setEnabled(False)
        self.formLayout_2 = QFormLayout(self.location)
        self.formLayout_2.setSpacing(6)
        self.formLayout_2.setContentsMargins(11, 11, 11, 11)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.labelLatitude = QLabel(self.location)
        self.labelLatitude.setObjectName(u"labelLatitude")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.labelLatitude)

        self.labelLongitude = QLabel(self.location)
        self.labelLongitude.setObjectName(u"labelLongitude")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.labelLongitude)

        self.inLatitude = QDoubleSpinBox(self.location)
        self.inLatitude.setObjectName(u"inLatitude")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.inLatitude)

        self.inLongitude = QDoubleSpinBox(self.location)
        self.inLongitude.setObjectName(u"inLongitude")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.inLongitude)


        self.verticalLayout.addWidget(self.location)


        self.verticalLayout_2.addWidget(self.automatic)

        self.checkSound = QCheckBox(self.centralWidget)
        self.checkSound.setObjectName(u"checkSound")

        self.verticalLayout_2.addWidget(self.checkSound)

        self.buttonApplication = QPushButton(self.centralWidget)
        self.buttonApplication.setObjectName(u"buttonApplication")

        self.verticalLayout_2.addWidget(self.buttonApplication)

        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.buttonSchedule.toggled.connect(self.time.setEnabled)
        self.buttonSun.toggled.connect(self.location.setEnabled)
        self.buttonLight.toggled.connect(self.buttonDark.setEnabled)
        self.buttonLight.toggled.connect(self.buttonLight.setDisabled)
        self.buttonLight.toggled.connect(self.automatic.setDisabled)
        self.buttonDark.toggled.connect(self.automatic.setDisabled)
        self.automatic.toggled.connect(self.manual.setDisabled)

        self.buttonLight.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Yin & Yang", None))
        self.imgLogo.setText("")
        self.buttonLight.setText(QCoreApplication.translate("MainWindow", u"Light", None))
        self.buttonDark.setText(QCoreApplication.translate("MainWindow", u"Dark", None))
        self.automatic.setTitle(QCoreApplication.translate("MainWindow", u"automatic", None))
        self.buttonSchedule.setText(QCoreApplication.translate("MainWindow", u"scheduled", None))
        self.labelLight.setText(QCoreApplication.translate("MainWindow", u"Light:", None))
        self.inTimeLight.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm", None))
        self.labelDark.setText(QCoreApplication.translate("MainWindow", u"Dark:", None))
        self.inTimeDark.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm", None))
        self.buttonSun.setText(QCoreApplication.translate("MainWindow", u"set sunset and sunrise", None))
        self.labelLatitude.setText(QCoreApplication.translate("MainWindow", u"Latitude:", None))
        self.labelLongitude.setText(QCoreApplication.translate("MainWindow", u"Longitude:", None))
        self.checkSound.setText(QCoreApplication.translate("MainWindow", u"enable sounds", None))
        self.buttonApplication.setText(QCoreApplication.translate("MainWindow", u"Select Applications", None))
    # retranslateUi

