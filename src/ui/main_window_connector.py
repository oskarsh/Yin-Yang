import logging

from PySide6 import QtWidgets
from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QScreen, QColor
from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialogButtonBox, QColorDialog

from src.ui.main_window import Ui_main_window

from src.yin_yang import set_desired_theme
from src.meta import ConfigEvent
from src.meta import PluginKey
from src.config import config, Modes, plugins, ConfigWatcher

logger = logging.getLogger(__name__)


class ConfigSaveNotifier(ConfigWatcher):
    def __init__(self):
        self.config_changed = False

    def notify(self, event: ConfigEvent, values: dict):
        match event:
            case ConfigEvent.CHANGE:
                self.config_changed = True
                logger.debug(values)
            case ConfigEvent.SAVE:
                self.config_changed = False


def reverse_dict_search(dictionary, value):
    return next(
        key for key, value_dict in dictionary.items()
        if value_dict == value
    )


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # basic setup
        self.setWindowTitle("Yin & Yang")
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self._config_watcher = ConfigSaveNotifier()
        config.add_event_listener(ConfigEvent.CHANGE, self._config_watcher)
        config.add_event_listener(ConfigEvent.SAVE, self._config_watcher)

        # center the window
        frame_gm = self.frameGeometry()
        center_point = QScreen.availableGeometry(self.screen()).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

        # set the config values to the elements
        self.load()

        # connects all buttons to the correct routes
        self.setup_config_sync()

    @property
    def config_changed(self) -> bool:
        return self._config_watcher.config_changed

    def load(self):
        """Sets the values from the config to the elements"""

        # set current version in statusbar
        self.ui.status_bar.showMessage(self.tr('You are using version {}', '')
                                       .format(str(config.version)))

        # set the correct mode
        mode = config.mode
        self.ui.btn_enable.setChecked(mode != Modes.MANUAL)

        if mode == Modes.FOLLOW_SUN:
            self.ui.time.setVisible(False)
            self.ui.btn_sun.setChecked(True)
        else:
            # fix that both settings for follow sun and scheduled showing up, when changing enabled
            self.ui.btn_schedule.setChecked(True)
            self.ui.location.setVisible(False)

        self.ui.toggle_sound.setChecked(config.get_plugin_key('sound', PluginKey.ENABLED))
        self.ui.toggle_notification.setChecked(config.get_plugin_key('notification', PluginKey.ENABLED))

        # sets the correct time based on config
        self.load_times()
        self.load_location()
        self.load_plugins()

    def load_times(self):
        """Loads the time from the config and sets it to the ui elements"""
        time_light, time_dark = config.times

        # giving the time widget the values of the config
        self.ui.inp_time_light.setTime(time_light)
        self.ui.inp_time_dark.setTime(time_dark)
        self.update_label_enabled()

    def load_location(self):
        if self.ui.btn_sun.isChecked():
            config.mode = Modes.FOLLOW_SUN
        self.ui.btn_location.setChecked(config.update_location)
        self.ui.location_input.setDisabled(config.update_location)
        # set correct coordinates
        coordinates = config.location
        self.ui.inp_latitude.setValue(coordinates[0])
        self.ui.inp_longitude.setValue(coordinates[1])

    def load_plugins(self):
        widget: QtWidgets.QGroupBox
        for plugin in plugins:
            # filter out plugins for application
            if plugin.name.casefold() in ['notification', 'sound']:
                continue

            widget = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, 'group' + plugin.name)
            if widget is None:
                widget = plugin.get_widget(self.ui.plugins_scroll_content)
                self.ui.plugins_scroll_content_layout.addWidget(widget)

            assert widget is not None, f'No widget for plugin {plugin.name} found'

            widget.toggled.connect(
                lambda enabled, p=plugin:
                config.update_plugin_key(p.name, PluginKey.ENABLED, enabled))

            if plugin.available_themes:
                # uses combobox instead of line edit
                for child in widget.findChildren(QtWidgets.QComboBox):
                    is_dark: bool = widget.findChildren(QtWidgets.QComboBox).index(child) == 1
                    child.currentTextChanged.connect(
                        lambda text, p=plugin, dark=is_dark: config.update_plugin_key(
                            p.name,
                            PluginKey.THEME_DARK if dark else PluginKey.THEME_LIGHT,
                            reverse_dict_search(p.available_themes, text)))
            else:
                children: [QtWidgets.QLineEdit] = widget.findChildren(QtWidgets.QLineEdit)
                children[0].textChanged.connect(
                    lambda text, p=plugin: config.update_plugin_key(p.name, PluginKey.THEME_LIGHT, text))
                children[1].textChanged.connect(
                    lambda text, p=plugin: config.update_plugin_key(p.name, PluginKey.THEME_DARK, text))

                if plugin.name == 'Wallpaper':
                    children: [QtWidgets.QPushButton] = widget.findChildren(QtWidgets.QDialogButtonBox)
                    children[0].clicked.connect(lambda: self.select_wallpaper(False))
                    children[1].clicked.connect(lambda: self.select_wallpaper(True))
                elif plugin.name == 'Brave':
                    buttons: [QtWidgets.QPushButton] = widget.findChildren(QtWidgets.QPushButton)
                    # this could be a loop, but it didn't work somehow
                    color_str_0 = config.get_plugin_key(plugin.name, PluginKey.THEME_LIGHT.value)
                    color_0 = QColor(color_str_0)
                    buttons[0].clicked.connect(lambda: self.select_color(False, color_0))

                    color_str_1 = config.get_plugin_key(plugin.name, PluginKey.THEME_DARK.value)
                    color_1 = QColor(color_str_1)
                    buttons[1].clicked.connect(lambda: self.select_color(True, color_1))
        plugin = None

    def update_label_enabled(self):
        time_light = self.ui.inp_time_light.time().toPython()
        time_dark = self.ui.inp_time_dark.time().toPython()
        self.ui.label_active.setText(
            self.tr('Dark mode will be active between {} and {}.')
            .format(time_dark.strftime("%H:%M"), time_light.strftime("%H:%M")))

    def setup_config_sync(self):
        # set sunrise and sunset times if mode is set to followSun or coordinates changed
        self.ui.btn_enable.toggled.connect(self.save_mode)
        self.ui.btn_schedule.toggled.connect(self.save_mode)
        self.ui.btn_sun.toggled.connect(self.save_mode)

        # buttons and inputs
        self.ui.btn_location.stateChanged.connect(self.update_location)
        self.ui.inp_latitude.valueChanged.connect(self.update_location)
        self.ui.inp_longitude.valueChanged.connect(self.update_location)
        self.ui.inp_time_light.timeChanged.connect(self.update_times)
        self.ui.inp_time_dark.timeChanged.connect(self.update_times)

        # connect dialog buttons
        self.ui.btn_box.clicked.connect(self.save_config_to_file)

        self.ui.toggle_sound.toggled.connect(
            lambda enabled: config.update_plugin_key('sound', PluginKey.ENABLED, enabled))
        self.ui.toggle_notification.toggled.connect(
            lambda enabled: config.update_plugin_key('notification', PluginKey.ENABLED, enabled))

    def save_mode(self):
        if not self.ui.btn_enable.isChecked():
            config.mode = Modes.MANUAL
        elif self.ui.btn_schedule.isChecked():
            config.mode = Modes.SCHEDULED
        elif self.ui.btn_sun.isChecked():
            config.mode = Modes.FOLLOW_SUN

        self.load_times()

    def update_times(self):
        if config.mode != Modes.SCHEDULED:
            return

        # update config if time has changed
        time_light = self.ui.inp_time_light.time().toPython()
        time_dark = self.ui.inp_time_dark.time().toPython()
        config.times = time_light, time_dark

        self.update_label_enabled()

    def update_location(self):
        if config.mode != Modes.FOLLOW_SUN:
            return

        config.update_location = self.ui.btn_location.isChecked()
        if config.update_location:
            self.load_location()
        else:
            self.ui.location_input.setEnabled(True)

            coordinates = [
                self.ui.inp_latitude.value(),
                self.ui.inp_longitude.value()
            ]
            config.location = coordinates
        # update message and times
        self.load_times()

    def select_wallpaper(self, dark: bool):
        message_light = self.tr('Open light wallpaper')
        message_dark = self.tr('Open dark wallpaper')
        file_name, _ = QFileDialog.getOpenFileName(
            self, message_dark if dark else message_light,
            QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)[0],
            'Images (*.png *.jpg *.jpeg *.JPG *.JPEG)')

        group_wallpaper = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, 'groupWallpaper')
        inputs_wallpaper = group_wallpaper.findChildren(QtWidgets.QLineEdit)
        i = 1 if dark else 0
        inputs_wallpaper[i].setText(file_name)

    def select_color(self, dark: bool, initial_color: QColor):
        selected_color = QColorDialog.getColor(initial_color)
        group_brave = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, 'groupBrave')
        inputs_brave = group_brave.findChildren(QtWidgets.QLineEdit)
        i = 1 if dark else 0
        inputs_brave[i].setText(selected_color.name())
        inputs_brave[i].setStyleSheet(f'background-color: {selected_color.name()};'
                                      f' color: {"white" if selected_color.lightness() <= 128 else "black"}')

    def save_config_to_file(self, button):
        """Saves the config to the file or restores values"""

        match button:
            case QDialogButtonBox.Apply:
                success = config.save()
                set_desired_theme(True)
                return success
            case QDialogButtonBox.RestoreDefaults:
                config.reset()
                self.load()
            case QDialogButtonBox.Cancel:
                self.close()
            case QDialogButtonBox.NoButton:
                raise ValueError(f'Unknown button {button}')
            case _:
                button = QDialogButtonBox.standardButton(self.ui.btn_box, button)
                return self.save_config_to_file(button)

    def should_close(self) -> bool:
        """Returns true if the user wants to close the application"""

        # ask the user if he wants to save changes
        if self.config_changed:
            message = self.tr('The settings have been modified. Do you want to save them?')
            ret = QMessageBox.warning(self, self.tr('Unsaved changes'),
                                      message,
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            match ret:
                case QMessageBox.Save:
                    # emulate click on apply-button
                    return self.save_config_to_file(QDialogButtonBox.Apply)
                case QMessageBox.Discard:
                    return True
                case QMessageBox.Cancel:
                    return False
                case _:
                    logger.warning('Unexpected return value from warning dialog.')
                    return False
        return True

    def closeEvent(self, event):
        """Overwrite the function that gets called when window is closed"""

        if self.should_close():
            event.accept()
        else:
            event.ignore()
