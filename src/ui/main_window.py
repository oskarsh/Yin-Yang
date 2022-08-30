# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialogButtonBox,
    QDoubleSpinBox, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTimeEdit, QVBoxLayout, QWidget)
import resources_rc

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(380, 633)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        main_window.setWindowTitle(u"Yin & Yang")
        icon = QIcon()
        iconThemeName = u"yin_yang"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u":/icons/logo", QSize(), QIcon.Normal, QIcon.Off)
        
        main_window.setWindowIcon(icon)
        main_window.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget_layout = QVBoxLayout(self.central_widget)
        self.central_widget_layout.setSpacing(6)
        self.central_widget_layout.setContentsMargins(11, 11, 11, 11)
        self.central_widget_layout.setObjectName(u"central_widget_layout")
        self.logo_layout = QHBoxLayout()
        self.logo_layout.setSpacing(6)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo = QLabel(self.central_widget)
        self.logo.setObjectName(u"logo")
        self.logo.setPixmap(QPixmap(u":/icons/logo"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(Qt.AlignCenter)

        self.logo_layout.addWidget(self.logo, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.central_widget_layout.addLayout(self.logo_layout)

        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setMinimumSize(QSize(368, 0))
        self.settings = QWidget()
        self.settings.setObjectName(u"settings")
        self.settings_layout = QVBoxLayout(self.settings)
        self.settings_layout.setSpacing(6)
        self.settings_layout.setContentsMargins(11, 11, 11, 11)
        self.settings_layout.setObjectName(u"settings_layout")
        self.btn_enable = QCheckBox(self.settings)
        self.btn_enable.setObjectName(u"btn_enable")
        self.btn_enable.setChecked(True)

        self.settings_layout.addWidget(self.btn_enable)

        self.schedule_settings = QWidget(self.settings)
        self.schedule_settings.setObjectName(u"schedule_settings")
        self.schedule_settings_layout = QVBoxLayout(self.schedule_settings)
        self.schedule_settings_layout.setSpacing(6)
        self.schedule_settings_layout.setContentsMargins(11, 11, 11, 11)
        self.schedule_settings_layout.setObjectName(u"schedule_settings_layout")
        self.line_top = QFrame(self.schedule_settings)
        self.line_top.setObjectName(u"line_top")
        self.line_top.setFrameShape(QFrame.HLine)
        self.line_top.setFrameShadow(QFrame.Sunken)

        self.schedule_settings_layout.addWidget(self.line_top)

        self.btn_schedule = QRadioButton(self.schedule_settings)
        self.btn_schedule.setObjectName(u"btn_schedule")
        self.btn_schedule.setChecked(True)

        self.schedule_settings_layout.addWidget(self.btn_schedule)

        self.time = QFrame(self.schedule_settings)
        self.time.setObjectName(u"time")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.time.sizePolicy().hasHeightForWidth())
        self.time.setSizePolicy(sizePolicy1)
        self.time_layout = QFormLayout(self.time)
        self.time_layout.setSpacing(6)
        self.time_layout.setContentsMargins(11, 11, 11, 11)
        self.time_layout.setObjectName(u"time_layout")
        self.time_layout.setLabelAlignment(Qt.AlignCenter)
        self.time_layout.setContentsMargins(37, -1, -1, -1)
        self.label_light = QLabel(self.time)
        self.label_light.setObjectName(u"label_light")
        self.label_light.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.time_layout.setWidget(0, QFormLayout.LabelRole, self.label_light)

        self.inp_time_light = QTimeEdit(self.time)
        self.inp_time_light.setObjectName(u"inp_time_light")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.inp_time_light.sizePolicy().hasHeightForWidth())
        self.inp_time_light.setSizePolicy(sizePolicy2)
        self.inp_time_light.setMinimumSize(QSize(88, 0))
        self.inp_time_light.setDisplayFormat(u"HH:mm")
        self.inp_time_light.setTime(QTime(8, 0, 0))

        self.time_layout.setWidget(0, QFormLayout.FieldRole, self.inp_time_light)

        self.label_dark = QLabel(self.time)
        self.label_dark.setObjectName(u"label_dark")
        self.label_dark.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.time_layout.setWidget(1, QFormLayout.LabelRole, self.label_dark)

        self.inp_time_dark = QTimeEdit(self.time)
        self.inp_time_dark.setObjectName(u"inp_time_dark")
        sizePolicy2.setHeightForWidth(self.inp_time_dark.sizePolicy().hasHeightForWidth())
        self.inp_time_dark.setSizePolicy(sizePolicy2)
        self.inp_time_dark.setMinimumSize(QSize(88, 0))
        self.inp_time_dark.setDisplayFormat(u"HH:mm")
        self.inp_time_dark.setTime(QTime(20, 0, 0))

        self.time_layout.setWidget(1, QFormLayout.FieldRole, self.inp_time_dark)


        self.schedule_settings_layout.addWidget(self.time)

        self.btn_sun = QRadioButton(self.schedule_settings)
        self.btn_sun.setObjectName(u"btn_sun")

        self.schedule_settings_layout.addWidget(self.btn_sun)

        self.location = QFrame(self.schedule_settings)
        self.location.setObjectName(u"location")
        self.verticalLayout = QVBoxLayout(self.location)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.location_input = QWidget(self.location)
        self.location_input.setObjectName(u"location_input")
        self.formLayout = QFormLayout(self.location_input)
        self.formLayout.setSpacing(6)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setObjectName(u"formLayout")
        self.label_longitude = QLabel(self.location_input)
        self.label_longitude.setObjectName(u"label_longitude")
        self.label_longitude.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_longitude)

        self.inp_longitude = QDoubleSpinBox(self.location_input)
        self.inp_longitude.setObjectName(u"inp_longitude")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.inp_longitude.sizePolicy().hasHeightForWidth())
        self.inp_longitude.setSizePolicy(sizePolicy3)
        self.inp_longitude.setMinimumSize(QSize(88, 0))
        self.inp_longitude.setSuffix(u"\u00b0")
        self.inp_longitude.setMinimum(-180.000000000000000)
        self.inp_longitude.setMaximum(180.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.inp_longitude)

        self.label_latitude = QLabel(self.location_input)
        self.label_latitude.setObjectName(u"label_latitude")
        self.label_latitude.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_latitude)

        self.inp_latitude = QDoubleSpinBox(self.location_input)
        self.inp_latitude.setObjectName(u"inp_latitude")
        sizePolicy2.setHeightForWidth(self.inp_latitude.sizePolicy().hasHeightForWidth())
        self.inp_latitude.setSizePolicy(sizePolicy2)
        self.inp_latitude.setMinimumSize(QSize(88, 0))
        self.inp_latitude.setSuffix(u"\u00b0")
        self.inp_latitude.setMinimum(-90.000000000000000)
        self.inp_latitude.setMaximum(90.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.inp_latitude)


        self.verticalLayout.addWidget(self.location_input)

        self.btn_location = QCheckBox(self.location)
        self.btn_location.setObjectName(u"btn_location")

        self.verticalLayout.addWidget(self.btn_location)


        self.schedule_settings_layout.addWidget(self.location)

        self.line_bottom = QFrame(self.schedule_settings)
        self.line_bottom.setObjectName(u"line_bottom")
        self.line_bottom.setFrameShape(QFrame.HLine)
        self.line_bottom.setFrameShadow(QFrame.Sunken)

        self.schedule_settings_layout.addWidget(self.line_bottom)


        self.settings_layout.addWidget(self.schedule_settings)

        self.toggle_sound = QCheckBox(self.settings)
        self.toggle_sound.setObjectName(u"toggle_sound")

        self.settings_layout.addWidget(self.toggle_sound)

        self.toggle_notification = QCheckBox(self.settings)
        self.toggle_notification.setObjectName(u"toggle_notification")

        self.settings_layout.addWidget(self.toggle_notification)

        self.label_active = QLabel(self.settings)
        self.label_active.setObjectName(u"label_active")
        self.label_active.setText(u"Darkmode will be active between")

        self.settings_layout.addWidget(self.label_active)

        self.space_vertical = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.settings_layout.addItem(self.space_vertical)

        self.tab_widget.addTab(self.settings, "")
        self.plugins = QWidget()
        self.plugins.setObjectName(u"plugins")
        self.plugins_layout = QVBoxLayout(self.plugins)
        self.plugins_layout.setSpacing(6)
        self.plugins_layout.setContentsMargins(11, 11, 11, 11)
        self.plugins_layout.setObjectName(u"plugins_layout")
        self.plugins_scroll = QScrollArea(self.plugins)
        self.plugins_scroll.setObjectName(u"plugins_scroll")
        self.plugins_scroll.setFrameShape(QFrame.NoFrame)
        self.plugins_scroll.setWidgetResizable(True)
        self.plugins_scroll_content = QWidget()
        self.plugins_scroll_content.setObjectName(u"plugins_scroll_content")
        self.plugins_scroll_content.setGeometry(QRect(0, 0, 348, 411))
        self.plugins_scroll_content_layout = QVBoxLayout(self.plugins_scroll_content)
        self.plugins_scroll_content_layout.setSpacing(6)
        self.plugins_scroll_content_layout.setContentsMargins(11, 11, 11, 11)
        self.plugins_scroll_content_layout.setObjectName(u"plugins_scroll_content_layout")
        self.plugins_scroll.setWidget(self.plugins_scroll_content)

        self.plugins_layout.addWidget(self.plugins_scroll)

        self.tab_widget.addTab(self.plugins, "")

        self.central_widget_layout.addWidget(self.tab_widget)

        self.btn_box = QDialogButtonBox(self.central_widget)
        self.btn_box.setObjectName(u"btn_box")
        self.btn_box.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.RestoreDefaults)

        self.central_widget_layout.addWidget(self.btn_box)

        main_window.setCentralWidget(self.central_widget)
        self.status_bar = QStatusBar(main_window)
        self.status_bar.setObjectName(u"status_bar")
        main_window.setStatusBar(self.status_bar)

        self.retranslateUi(main_window)
        self.btn_sun.toggled.connect(self.location.setVisible)
        self.btn_schedule.toggled.connect(self.time.setVisible)
        self.btn_enable.toggled.connect(self.schedule_settings.setVisible)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        self.btn_enable.setText(QCoreApplication.translate("main_window", u"Automatic theme switching", None))
        self.btn_schedule.setText(QCoreApplication.translate("main_window", u"Custom Schedule", None))
        self.label_light.setText(QCoreApplication.translate("main_window", u"Light:", None))
        self.label_dark.setText(QCoreApplication.translate("main_window", u"Dark:", None))
        self.btn_sun.setText(QCoreApplication.translate("main_window", u"Sunset to Sunrise", None))
        self.label_longitude.setText(QCoreApplication.translate("main_window", u"Longitude:", None))
        self.label_latitude.setText(QCoreApplication.translate("main_window", u"Latitude:", None))
        self.btn_location.setText(QCoreApplication.translate("main_window", u"update automatically", None))
        self.toggle_sound.setText(QCoreApplication.translate("main_window", u"Make a sound when switching the theme", None))
        self.toggle_notification.setText(QCoreApplication.translate("main_window", u"Send a notification", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.settings), QCoreApplication.translate("main_window", u"Settings", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.plugins), QCoreApplication.translate("main_window", u"Plugins", None))
        pass
    # retranslateUi

