# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys


class Ui_MainWindow(object):

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(300, 360)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(300, 360))
        MainWindow.setMaximumSize(QtCore.QSize(300, 360))
        MainWindow.setBaseSize(QtCore.QSize(300, 360))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/icon.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 50, 251, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.yinyang_img = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(128)
        sizePolicy.setVerticalStretch(128)
        sizePolicy.setHeightForWidth(
            self.yinyang_img.sizePolicy().hasHeightForWidth())
        self.yinyang_img.setSizePolicy(sizePolicy)
        self.yinyang_img.setMinimumSize(QtCore.QSize(100, 100))
        self.yinyang_img.setMaximumSize(QtCore.QSize(100, 275))
        self.yinyang_img.setSizeIncrement(QtCore.QSize(0, 0))
        self.yinyang_img.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.yinyang_img.setFont(font)
        self.yinyang_img.setText("")
        self.yinyang_img.setTextFormat(QtCore.Qt.RichText)
        self.yinyang_img.setPixmap(QtGui.QPixmap(
            sys._MEIPASS+"/assets/yin-yang.svg"))
        self.yinyang_img.setScaledContents(False)
        self.yinyang_img.setAlignment(QtCore.Qt.AlignCenter)
        self.yinyang_img.setObjectName("yinyang_img")
        self.verticalLayout.addWidget(
            self.yinyang_img, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.light_push = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.light_push.setAutoDefault(False)
        self.light_push.setDefault(False)
        self.light_push.setFlat(False)
        self.light_push.setObjectName("light_push")
        self.horizontalLayout.addWidget(self.light_push)
        self.dark_push = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.dark_push.setEnabled(False)
        self.dark_push.setObjectName("dark_push")
        self.horizontalLayout.addWidget(self.dark_push)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.schedule_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.schedule_radio.setObjectName("schedule_radio")
        self.verticalLayout.addWidget(self.schedule_radio)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setHorizontalSpacing(40)
        self.formLayout.setVerticalSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.light_time = QtWidgets.QTimeEdit(self.verticalLayoutWidget)
        self.light_time.setEnabled(False)
        self.light_time.setTime(QtCore.QTime(8, 0, 0))
        self.light_time.setObjectName("light_time")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.light_time)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.dark_time = QtWidgets.QTimeEdit(self.verticalLayoutWidget)
        self.dark_time.setEnabled(False)
        self.dark_time.setTime(QtCore.QTime(20, 0, 0))
        self.dark_time.setObjectName("dark_time")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.dark_time)
        self.verticalLayout.addLayout(self.formLayout)
        self.settings_push = QtWidgets.QPushButton(self.centralWidget)
        self.settings_push.setGeometry(QtCore.QRect(210, 10, 83, 25))
        self.settings_push.setObjectName("settings_push")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Yin & Yang"))
        self.light_push.setText(_translate("MainWindow", "Light"))
        self.dark_push.setText(_translate("MainWindow", "Dark"))
        self.schedule_radio.setText(_translate("MainWindow", "scheduled"))
        self.label.setText(_translate("MainWindow", "Light:"))
        self.light_time.setDisplayFormat(_translate("MainWindow", "HH:mm"))
        self.label_2.setText(_translate("MainWindow", "Dark:"))
        self.dark_time.setDisplayFormat(_translate("MainWindow", "HH:mm"))
        self.settings_push.setText(_translate("MainWindow", "Settings"))
