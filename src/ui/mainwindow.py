# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(271, 523)
        MainWindow.setMinimumSize(QtCore.QSize(271, 0))
        MainWindow.setMaximumSize(QtCore.QSize(271, 523))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/assets/yin-yang.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logo = QtWidgets.QHBoxLayout()
        self.logo.setSpacing(6)
        self.logo.setObjectName("logo")
        self.imgLogo = QtWidgets.QLabel(self.centralWidget)
        self.imgLogo.setPixmap(QtGui.QPixmap(":/icons/assets/yin-yang.svg"))
        self.imgLogo.setScaledContents(True)
        self.imgLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.imgLogo.setObjectName("imgLogo")
        self.logo.addWidget(self.imgLogo, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addLayout(self.logo)
        self.manual = QtWidgets.QWidget(self.centralWidget)
        self.manual.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual.sizePolicy().hasHeightForWidth())
        self.manual.setSizePolicy(sizePolicy)
        self.manual.setObjectName("manual")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.manual)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonLight = QtWidgets.QPushButton(self.manual)
        self.buttonLight.setAutoDefault(False)
        self.buttonLight.setDefault(False)
        self.buttonLight.setFlat(False)
        self.buttonLight.setObjectName("buttonLight")
        self.horizontalLayout.addWidget(self.buttonLight)
        self.buttonDark = QtWidgets.QPushButton(self.manual)
        self.buttonDark.setObjectName("buttonDark")
        self.horizontalLayout.addWidget(self.buttonDark)
        self.verticalLayout_2.addWidget(self.manual)
        self.automatic = QtWidgets.QGroupBox(self.centralWidget)
        self.automatic.setCheckable(True)
        self.automatic.setChecked(True)
        self.automatic.setObjectName("automatic")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.automatic)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonSchedule = QtWidgets.QRadioButton(self.automatic)
        self.buttonSchedule.setChecked(True)
        self.buttonSchedule.setObjectName("buttonSchedule")
        self.verticalLayout.addWidget(self.buttonSchedule)
        self.time = QtWidgets.QFrame(self.automatic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time.sizePolicy().hasHeightForWidth())
        self.time.setSizePolicy(sizePolicy)
        self.time.setObjectName("time")
        self.formLayout = QtWidgets.QFormLayout(self.time)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setHorizontalSpacing(40)
        self.formLayout.setVerticalSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.labelLight = QtWidgets.QLabel(self.time)
        self.labelLight.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLight.setObjectName("labelLight")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelLight)
        self.inTimeLight = QtWidgets.QTimeEdit(self.time)
        self.inTimeLight.setTime(QtCore.QTime(8, 0, 0))
        self.inTimeLight.setObjectName("inTimeLight")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inTimeLight)
        self.labelDark = QtWidgets.QLabel(self.time)
        self.labelDark.setObjectName("labelDark")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelDark)
        self.inTimeDark = QtWidgets.QTimeEdit(self.time)
        self.inTimeDark.setTime(QtCore.QTime(20, 0, 0))
        self.inTimeDark.setObjectName("inTimeDark")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inTimeDark)
        self.verticalLayout.addWidget(self.time)
        self.buttonSun = QtWidgets.QRadioButton(self.automatic)
        self.buttonSun.setObjectName("buttonSun")
        self.verticalLayout.addWidget(self.buttonSun)
        self.location = QtWidgets.QFrame(self.automatic)
        self.location.setEnabled(False)
        self.location.setObjectName("location")
        self.formLayout_2 = QtWidgets.QFormLayout(self.location)
        self.formLayout_2.setContentsMargins(11, 11, 11, 11)
        self.formLayout_2.setSpacing(6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelLatitude = QtWidgets.QLabel(self.location)
        self.labelLatitude.setObjectName("labelLatitude")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelLatitude)
        self.labelLongitude = QtWidgets.QLabel(self.location)
        self.labelLongitude.setObjectName("labelLongitude")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelLongitude)
        self.inLatitude = QtWidgets.QDoubleSpinBox(self.location)
        self.inLatitude.setMinimum(-90.0)
        self.inLatitude.setMaximum(90.0)
        self.inLatitude.setObjectName("inLatitude")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inLatitude)
        self.inLongitude = QtWidgets.QDoubleSpinBox(self.location)
        self.inLongitude.setMinimum(-180.0)
        self.inLongitude.setMaximum(180.0)
        self.inLongitude.setObjectName("inLongitude")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inLongitude)
        self.verticalLayout.addWidget(self.location)
        self.verticalLayout_2.addWidget(self.automatic)
        self.checkSound = QtWidgets.QCheckBox(self.centralWidget)
        self.checkSound.setObjectName("checkSound")
        self.verticalLayout_2.addWidget(self.checkSound)
        self.buttonApplication = QtWidgets.QPushButton(self.centralWidget)
        self.buttonApplication.setObjectName("buttonApplication")
        self.verticalLayout_2.addWidget(self.buttonApplication)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.buttonSchedule.toggled['bool'].connect(self.time.setEnabled)
        self.buttonSun.toggled['bool'].connect(self.location.setEnabled)
        self.buttonLight.toggled['bool'].connect(self.buttonDark.setEnabled)
        self.buttonLight.toggled['bool'].connect(self.buttonLight.setDisabled)
        self.buttonLight.toggled['bool'].connect(self.automatic.setDisabled)
        self.buttonDark.toggled['bool'].connect(self.automatic.setDisabled)
        self.automatic.toggled['bool'].connect(self.manual.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Yin & Yang"))
        self.buttonLight.setText(_translate("MainWindow", "Light"))
        self.buttonDark.setText(_translate("MainWindow", "Dark"))
        self.automatic.setTitle(_translate("MainWindow", "automatic"))
        self.buttonSchedule.setText(_translate("MainWindow", "scheduled"))
        self.labelLight.setText(_translate("MainWindow", "Light:"))
        self.inTimeLight.setDisplayFormat(_translate("MainWindow", "HH:mm"))
        self.labelDark.setText(_translate("MainWindow", "Dark:"))
        self.inTimeDark.setDisplayFormat(_translate("MainWindow", "HH:mm"))
        self.buttonSun.setText(_translate("MainWindow", "set sunset and sunrise"))
        self.labelLatitude.setText(_translate("MainWindow", "Latitude:"))
        self.labelLongitude.setText(_translate("MainWindow", "Longitude:"))
        self.inLatitude.setSuffix(_translate("MainWindow", "°"))
        self.inLongitude.setSuffix(_translate("MainWindow", "°"))
        self.checkSound.setText(_translate("MainWindow", "enable sounds"))
        self.buttonApplication.setText(_translate("MainWindow", "Select Applications"))
import resources_rc
