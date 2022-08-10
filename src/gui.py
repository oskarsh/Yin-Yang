import logging
import subprocess
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog

from src.config import config, plugins, Modes
from src.ui.mainwindow import Ui_MainWindow
from src.ui.settings import Ui_MainWindow as Ui_SettingsWindow
from src import yin_yang

logger = logging.getLogger(__name__)


class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        # center the settings window
        self.center()
        # syncing with config - fill out all fields based on Config
        self.sync_with_config()
        # register all the handler onClick functions ...
        self.register_handlers()

    def close_event(self, event):
        """Overwrite the function that gets called when window is closed"""
        self.save_and_exit()

    def save_and_exit(self):
        logger.debug("saving options")

        for plugin in plugins:
            widget: QtWidgets.QGroupBox = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, f'group{plugin.name}')

            plugin.enabled = widget.isChecked()
            if plugin.available_themes:
                # extra behaviour for combobox
                children = widget.findChildren(QtWidgets.QComboBox)
                for child in children:
                    theme_name: str = list(plugin.available_themes.keys())[child.currentIndex()]
                    if children.index(child) == 0:
                        # dropdown for light theme selected
                        plugin.theme_light = theme_name
                    else:
                        plugin.theme_dark = theme_name
            else:
                if plugin.name == 'Wallpaper':
                    continue
                children = widget.findChildren(QtWidgets.QLineEdit)
                plugin.theme_light = children[0].text()
                plugin.theme_dark = children[1].text()

        # showing the main window and hiding the current one
        self.hide()
        self.window = MainWindow()
        self.window.show()

    def register_handlers(self):
        self.ui.back_button.clicked.connect(self.save_and_exit)

    def sync_with_config(self):
        """Adds the plugin widgets to the ui"""
        widget: QtWidgets.QGroupBox
        for plugin in plugins:

            widget = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, 'group' + plugin.name)
            if widget is None:
                widget = plugin.get_widget(self.ui.plugins_scroll_content)
                self.ui.plugins_scroll_content_layout.addWidget(widget)

            assert widget is not None, f'No widget for plugin {plugin.name} found'

            widget.setChecked(plugin.enabled)

            if plugin.name == 'Wallpaper':
                children = widget.findChildren(QtWidgets.QPushButton)
                children[0].clicked.connect(self.open_wallpaper_light)
                children[1].clicked.connect(self.open_wallpaper_dark)

            if plugin.available_themes:
                # uses combobox instead of line edit
                # set the index
                for child in widget.findChildren(QtWidgets.QComboBox):
                    light_mode: bool = widget.findChildren(QtWidgets.QComboBox).index(child) == 0
                    used_theme: str = plugin.theme_light if light_mode else plugin.theme_dark
                    index: int
                    if used_theme == '':
                        index = 0
                    else:
                        index = child.findText(
                            plugin.available_themes[
                                used_theme
                            ]
                        )
                    child.setCurrentIndex(index)
            elif plugin.name != 'Wallpaper':
                children = widget.findChildren(QtWidgets.QLineEdit)
                children[0].setText(plugin.theme_light)
                children[1].setText(plugin.theme_dark)

            if not plugin.available:
                widget.setEnabled(False)

    def open_wallpaper_light(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Wallpaper Light", "")
        subprocess.run(["notify-send", "Light Wallpaper set"])
        config.update("wallpaperLightTheme", file_name)

    def open_wallpaper_dark(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Wallpaper Dark", "")
        subprocess.run(["notify-send", "Dark Wallpaper set"])
        config.update("wallpaperDarkTheme", file_name)

    def center(self):
        frame_gm = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yin-Yang")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # center itself
        self.center()
        # connects all buttons to the correct routes
        self.register_handlers()
        # syncs the UI with the config
        self.sync_with_config()

    def center(self):
        frame_gm = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def register_handlers(self):
        # connect the "light" button
        self.ui.light_push.clicked.connect(self.toggle_light)
        # connect the "dark" button
        self.ui.dark_push.clicked.connect(self.toggle_dark)
        # connect the settingsButton
        self.ui.settings_push.clicked.connect(self.open_settings)
        # connect the sound checkbox
        self.ui.sound_checkBox.clicked.connect(self.toggle_sound)
        # connect the time change with the correct function
        self.ui.light_time.timeChanged.connect(self.time_changed)
        self.ui.dark_time.timeChanged.connect(self.time_changed)
        self.ui.schedule_radio.toggled.connect(self.toggle_schedule_cliked)

    def sync_with_config(self):
        # sets the scheduled button to be enabled or disabled
        if config.mode == Modes.scheduled:
            self.ui.schedule_radio.setChecked(True)
            self.ui.dark_time.setEnabled(True)
            self.ui.light_time.setEnabled(True)
            yin_yang.start_daemon()
        # sets the correct time based on config
        self.set_correct_time()
        # setting the correct buttons based on config "dark"  "light"
        self.set_correct_buttons()

    def open_settings(self):
        self.secwindow = SettingsWindow()
        self.secwindow.setWindowTitle("Settings")
        self.secwindow.show()
        self.hide()

    def toggle_light(self):
        yin_yang.switch_to_light()
        self.sync_with_config()
        # experimental
        # self.restart()

    def toggle_dark(self):
        yin_yang.switch_to_dark()
        self.sync_with_config()
        # self.restart()

    def toggle_sound(self):
        config.update("soundEnabled", self.ui.sound_checkBox.isChecked())
        self.sync_with_config()

    # no needed since QT is now used system wise instead of python wise
    def restart(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def set_correct_time(self):
        time_light, time_dark = config.times

        # giving the time widget the values of the config
        dark_time = QTime(time_dark)
        light_time = QTime(time_light)
        self.ui.dark_time.setTime(dark_time)
        self.ui.light_time.setTime(light_time)

    def set_correct_buttons(self):
        if config.dark_mode:
            self.ui.light_push.setEnabled(True)
            self.ui.dark_push.setEnabled(False)
        else:
            self.ui.light_push.setEnabled(False)
            self.ui.dark_push.setEnabled(True)
        if config.mode == Modes.manual:
            self.ui.light_push.setEnabled(True)
            self.ui.dark_push.setEnabled(True)

    def time_changed(self):
        # update config if time has changed
        if config.mode == Modes.scheduled:
            time_light = self.ui.light_time.time().toPyTime()
            time_dark = self.ui.dark_time.time().toPyTime()
            config.times = time_light, time_dark

    def toggle_schedule_cliked(self):
        checked = self.ui.schedule_radio.isChecked()
        config.update("schedule", checked)
        if checked:
            self.ui.dark_time.setEnabled(True)
            self.ui.light_time.setEnabled(True)
        else:
            self.ui.dark_time.setEnabled(False)
            self.ui.light_time.setEnabled(False)
