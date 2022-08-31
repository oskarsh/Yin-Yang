from PySide6 import QtWidgets
from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialogButtonBox

from src.ui.main_window import Ui_main_window
from src.config import config, Modes, plugins


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # basic setup
        self.setWindowTitle("Yin & Yang")
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        # center the window
        frame_gm = self.frameGeometry()
        center_point = QScreen.availableGeometry(self.screen()).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

        # set the config values to the elements
        self.load()

        # connects all buttons to the correct routes
        self.register_handlers()

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

        self.ui.toggle_sound.setChecked(config.get(plugin='sound', key='enabled'))
        self.ui.toggle_notification.setChecked(config.get(plugin='notification', key='enabled'))

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
        widget: QtWidgets.QWidget
        for plugin in plugins:
            # filter out plugins for application
            if plugin.name.casefold() in ['notification', 'sound']:
                continue

            widget: QtWidgets.QGroupBox = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox,
                                                                                   'group' + plugin.name)
            if widget is None:
                widget = plugin.get_widget(self.ui.plugins_scroll_content)
                self.ui.plugins_scroll_content_layout.addWidget(widget)

            assert widget is not None, f'No widget for plugin {plugin.name} found'

            widget.setChecked(config.get(plugin.name, 'Enabled'))

            if plugin.name == 'Wallpaper':
                children: [QtWidgets.QPushButton] = widget.findChildren(QtWidgets.QDialogButtonBox)
                children[0].clicked.connect(lambda: self.save_wallpaper(False))
                children[1].clicked.connect(lambda: self.save_wallpaper(True))

                children: [QtWidgets.QLineEdit] = widget.findChildren(QtWidgets.QLineEdit)
                children[0].setText(plugin.theme_light)
                children[1].setText(plugin.theme_dark)

                continue

            if plugin.available_themes:
                # uses combobox instead of line edit
                # set the index
                for child in widget.findChildren(QtWidgets.QComboBox):
                    is_dark_checkbox: bool = widget.findChildren(QtWidgets.QComboBox).index(child) == 1
                    used_theme: str = plugin.theme_dark if is_dark_checkbox else plugin.theme_light
                    index: int
                    if used_theme == '':
                        index = 0
                    else:
                        index = child.findText(
                            plugin.available_themes[used_theme]
                        )
                    child.setCurrentIndex(index)
            else:
                children = widget.findChildren(QtWidgets.QLineEdit)
                children[0].setText(plugin.theme_light)
                children[1].setText(plugin.theme_dark)

    def update_label_enabled(self):
        time_light = self.ui.inp_time_light.time().toPython()
        time_dark = self.ui.inp_time_dark.time().toPython()
        self.ui.label_active.setText(
            self.tr('Dark mode will be active between {} and {}.')
                .format(time_dark.strftime("%H:%M"), time_light.strftime("%H:%M")))

    def register_handlers(self):
        # set sunrise and sunset times if mode is set to followSun or coordinates changed
        self.ui.btn_enable.toggled.connect(self.save_mode)
        self.ui.btn_schedule.toggled.connect(self.save_mode)
        self.ui.btn_sun.toggled.connect(self.save_mode)

        # buttons and inputs
        self.ui.btn_location.stateChanged.connect(self.save_location)
        self.ui.inp_latitude.valueChanged.connect(self.save_location)
        self.ui.inp_longitude.valueChanged.connect(self.save_location)
        self.ui.inp_time_light.timeChanged.connect(self.save_times)
        self.ui.inp_time_dark.timeChanged.connect(self.save_times)

        # connect dialog buttons
        self.ui.btn_box.clicked.connect(self.save_config_to_file)

    def save(self):
        """Sets the values to the config object, but does not save them"""

        config.update('sound', 'enabled', self.ui.toggle_sound.isChecked())
        config.update('notification', 'enabled', self.ui.toggle_notification.isChecked())
        self.save_plugins()

    def save_mode(self):
        if not self.ui.btn_enable.isChecked():
            config.mode = Modes.MANUAL
        elif self.ui.btn_schedule.isChecked():
            config.mode = Modes.SCHEDULED
        elif self.ui.btn_sun.isChecked():
            config.mode = Modes.FOLLOW_SUN

        self.load_times()

    def save_times(self):
        """Sets the time set in the ui to the config"""

        if config.mode != Modes.SCHEDULED:
            return

        # update config if time has changed
        time_light = self.ui.inp_time_light.time().toPython()
        time_dark = self.ui.inp_time_dark.time().toPython()
        config.times = time_light, time_dark

        self.update_label_enabled()

    def save_location(self):
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
        # update message
        self.load_times()

    def save_plugins(self):
        for plugin in plugins:
            # filter out all plugins for application
            if plugin.name.casefold() in ['notification', 'sound']:
                continue

            widget = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, f'group{plugin.name}')

            config.update(plugin.name, 'enabled', widget.isChecked())
            if plugin.available_themes:
                # extra behaviour for combobox
                children = widget.findChildren(QtWidgets.QComboBox)
                for child in children:
                    theme = 'light' if children.index(child) == 0 else 'dark'
                    theme_name: str = list(plugin.available_themes.keys())[child.currentIndex()]
                    config.update(plugin.name, f'{theme}_theme', theme_name)
            else:
                children = widget.findChildren(QtWidgets.QLineEdit)
                config.update(plugin.name, 'light_theme', children[0].text())
                config.update(plugin.name, 'dark_theme', children[1].text())

    def save_wallpaper(self, dark: bool):
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

    def save_config_to_file(self, button):
        """Saves the config to the file or restores values"""

        button = QDialogButtonBox.standardButton(self.ui.btn_box, button)
        if button == QDialogButtonBox.Apply:
            self.save()
            return config.write()
        elif button == QDialogButtonBox.RestoreDefaults:
            config.set_default()
            self.load()
        elif button == QDialogButtonBox.Cancel:
            self.close()
        else:
            raise ValueError(f'Unknown button {button}')

    def should_close(self) -> bool:
        """Returns true if the user wants to close the application"""

        # ask the user if he wants to save changes
        if config.changed:
            message = self.tr('The settings have been modified. Do you want to save them?')
            ret = QMessageBox.warning(self, self.tr('Unsaved changes'),
                                      message,
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return config.write()
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def close(self):
        """Overwrite the function that gets called when window is closed"""

        if self.should_close():
            super().close()
        else:
            pass
