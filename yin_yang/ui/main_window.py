# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialogButtonBox, QDoubleSpinBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QTimeEdit, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(550, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        main_window.setMinimumSize(QSize(400, 600))
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

        self.manual_buttons = QWidget(self.settings)
        self.manual_buttons.setObjectName(u"manual_buttons")
        self.horizontalLayout_3 = QHBoxLayout(self.manual_buttons)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.button_light = QPushButton(self.manual_buttons)
        self.button_light.setObjectName(u"button_light")

        self.horizontalLayout_3.addWidget(self.button_light)

        self.button_dark = QPushButton(self.manual_buttons)
        self.button_dark.setObjectName(u"button_dark")

        self.horizontalLayout_3.addWidget(self.button_dark)


        self.settings_layout.addWidget(self.manual_buttons)

        self.toggle_notification = QCheckBox(self.settings)
        self.toggle_notification.setObjectName(u"toggle_notification")

        self.settings_layout.addWidget(self.toggle_notification)

        self.bootOffsetSettings = QFormLayout()
        self.bootOffsetSettings.setSpacing(6)
        self.bootOffsetSettings.setObjectName(u"bootOffsetSettings")
        self.bootOffsetLabel = QLabel(self.settings)
        self.bootOffsetLabel.setObjectName(u"bootOffsetLabel")

        self.bootOffsetSettings.setWidget(0, QFormLayout.LabelRole, self.bootOffsetLabel)

        self.bootOffset = QSpinBox(self.settings)
        self.bootOffset.setObjectName(u"bootOffset")
        self.bootOffset.setValue(10)

        self.bootOffsetSettings.setWidget(0, QFormLayout.FieldRole, self.bootOffset)


        self.settings_layout.addLayout(self.bootOffsetSettings)

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
        self.plugins_scroll_content.setGeometry(QRect(0, 0, 501, 86))
        self.plugins_scroll_content_layout = QVBoxLayout(self.plugins_scroll_content)
        self.plugins_scroll_content_layout.setSpacing(6)
        self.plugins_scroll_content_layout.setContentsMargins(11, 11, 11, 11)
        self.plugins_scroll_content_layout.setObjectName(u"plugins_scroll_content_layout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.samplePluginGroupBox = QGroupBox(self.plugins_scroll_content)
        self.samplePluginGroupBox.setObjectName(u"samplePluginGroupBox")
        self.samplePluginGroupBox.setTitle(u"Sample Plugin")
        self.horizontalLayout_2 = QHBoxLayout(self.samplePluginGroupBox)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox = QComboBox(self.samplePluginGroupBox)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setCurrentText(u"")
        self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox.setPlaceholderText(u"firefox-compact-light@mozilla.org")

        self.horizontalLayout_2.addWidget(self.comboBox)

        self.comboBox_2 = QComboBox(self.samplePluginGroupBox)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setCurrentText(u"")
        self.comboBox_2.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox_2.setPlaceholderText(u"firefox-compact-dark@mozilla.org")

        self.horizontalLayout_2.addWidget(self.comboBox_2)


        self.horizontalLayout.addWidget(self.samplePluginGroupBox)


        self.plugins_scroll_content_layout.addLayout(self.horizontalLayout)

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
        self.btn_enable.toggled.connect(self.manual_buttons.setHidden)

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
        self.btn_location.setText(QCoreApplication.translate("main_window", u"update location automatically", None))
        self.button_light.setText(QCoreApplication.translate("main_window", u"Light", None))
        self.button_dark.setText(QCoreApplication.translate("main_window", u"Dark", None))
        self.toggle_notification.setText(QCoreApplication.translate("main_window", u"Send a notification", None))
#if QT_CONFIG(tooltip)
        self.bootOffsetLabel.setToolTip(QCoreApplication.translate("main_window", u"Time to wait until the system finished booting. Default value is 10 seconds.", None))
#endif // QT_CONFIG(tooltip)
        self.bootOffsetLabel.setText(QCoreApplication.translate("main_window", u"Delay after boot:", None))
        self.bootOffset.setSuffix(QCoreApplication.translate("main_window", u"s", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.settings), QCoreApplication.translate("main_window", u"Settings", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.plugins), QCoreApplication.translate("main_window", u"Plugins", None))
        pass
    # retranslateUi

