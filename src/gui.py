import subprocess
import pwd
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog
from src.ui.mainwindow import Ui_MainWindow
from src.ui.settings import Ui_MainWindow as Ui_SettingsWindow
from src import yin_yang
from src import config


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
        print("saving options")

        kde_light_short = self.ui.kde_combo_light.currentText()
        kde_dark_short = self.ui.kde_combo_dark.currentText()

        config.update("kdeLightTheme",
                      self.get_kde_theme_long(kde_light_short))
        config.update("kdeDarkTheme", self.get_kde_theme_long(kde_dark_short))
        config.update("kdeEnabled", self.ui.kde_checkbox.isChecked())

        config.update("codeLightTheme", self.ui.code_line_light.text())
        config.update("codeDarkTheme", self.ui.code_line_dark.text())
        config.update("codeEnabled", self.ui.code_checkbox.isChecked())

        config.update("gtkLightTheme", self.ui.gtk_line_light.text())
        config.update("gtkDarkTheme", self.ui.gtk_line_dark.text())
        config.update("gtkEnabled", self.ui.gtk_checkbox.isChecked())

        config.update("kvantumLightTheme", self.ui.kvantum_line_light.text())
        config.update("kvantumDarkTheme", self.ui.kvantum_line_dark.text())
        config.update("kvantumEnabled", self.ui.kvantum_checkbox.isChecked())

        config.update("atomLightTheme", self.ui.atom_line_light.text())
        config.update("atomDarkTheme", self.ui.atom_line_dark.text())
        config.update("atomEnabled", self.ui.atom_checkbox.isChecked())

        # showing the main window and hiding the current one
        self.hide()
        self.window = MainWindow()
        self.window.show()

    def register_handlers(self):
        self.ui.kde_checkbox.toggled.connect(self.toggle_kde_fields)
        self.ui.code_checkbox.toggled.connect(self.toggle_code_fields)
        self.ui.gtk_checkbox.toggled.connect(self.toggle_gtk_fields)
        self.ui.kvantum_checkbox.toggled.connect(self.toggle_kvantum_fields)
        self.ui.atom_checkbox.toggled.connect(self.toggle_atom_fields)
        self.ui.wallpaper_button_light.clicked.connect(
            self.open_wallpaper_light)
        self.ui.wallpaper_button_dark.clicked.connect(self.open_wallpaper_dark)
        self.ui.wallpaper_checkbox.toggled.connect(
            self.toggle_wallpaper_buttons)
        self.ui.back_button.clicked.connect(self.save_and_exit)

    def sync_with_config(self):
        # sync config label with get the correct version
        self.ui.version_label.setText("yin-yang: v" + str(config.get_version()))
        # syncing all fields and checkboxes with config
        # ---- KDE -----
        # reads out all kde themes and displays them inside a combobox
        if config.get("kdeEnabled"):
            # fixed bug where themes get appended multiple times
            self.get_kde_themes()

            self.ui.kde_checkbox.setChecked(config.get("kdeEnabled"))
            self.ui.kde_combo_dark.setEnabled(config.get("kdeEnabled"))
            self.ui.kde_combo_light.setEnabled(config.get("kdeEnabled"))
            index_light = self.ui.kde_combo_light.findText(
                self.get_kde_theme_short(config.get("kdeLightTheme")))
            self.ui.kde_combo_light.setCurrentIndex(index_light)
            index_dark = self.ui.kde_combo_dark.findText(
                self.get_kde_theme_short(config.get("kdeDarkTheme")))
            self.ui.kde_combo_dark.setCurrentIndex(index_dark)
        # ---- VSCode ----
        self.ui.code_line_light.setText(config.get("codeLightTheme"))
        self.ui.code_line_light.setEnabled(config.get("codeEnabled"))
        self.ui.code_line_dark.setText(config.get("codeDarkTheme"))
        self.ui.code_line_dark.setEnabled(config.get("codeEnabled"))
        self.ui.code_checkbox.setChecked(config.get("codeEnabled"))
        # ---- GTK -----
        self.ui.gtk_line_light.setText(config.get("gtkLightTheme"))
        self.ui.gtk_line_dark.setText(config.get("gtkDarkTheme"))
        self.ui.gtk_checkbox.setChecked(config.get("gtkEnabled"))
        self.ui.gtk_line_light.setEnabled(config.get("gtkEnabled"))
        self.ui.gtk_line_dark.setEnabled(config.get("gtkEnabled"))
        # ---- Kvantum -----
        self.ui.kvantum_line_light.setText(config.get("kvantumLightTheme"))
        self.ui.kvantum_line_dark.setText(config.get("kvantumDarkTheme"))
        self.ui.kvantum_checkbox.setChecked(config.get("kvantumEnabled"))
        self.ui.kvantum_line_light.setEnabled(config.get("kvantumEnabled"))
        self.ui.kvantum_line_dark.setEnabled(config.get("kvantumEnabled"))
        # ----- wallpaper --------
        self.ui.wallpaper_button_light.setEnabled(
            config.get("wallpaperEnabled"))
        self.ui.wallpaper_button_dark.setEnabled(
            config.get("wallpaperEnabled"))
        self.ui.wallpaper_checkbox.setChecked(config.get("wallpaperEnabled"))
        # ----- Atom --------
        self.ui.atom_line_light.setText(config.get("atomLightTheme"))
        self.ui.atom_line_dark.setText(config.get("atomDarkTheme"))
        self.ui.atom_checkbox.setChecked(config.get("atomEnabled"))
        self.ui.atom_line_light.setEnabled(config.get("atomEnabled"))
        self.ui.atom_line_dark.setEnabled(config.get("atomEnabled"))

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

    def get_kde_themes(self):
        """
        Sends the kde themes to the ui.
        """
        if config.get("desktop") == "kde":
            if (self.ui.kde_combo_light.count() == 0 and self.ui.kde_combo_dark.count() == 0):
                kde_themes = self.get_kde_theme_names()

                for name, theme in kde_themes.items():
                    self.ui.kde_combo_light.addItem(name)
                    self.ui.kde_combo_dark.addItem(name)
        else:
            self.ui.kde_combo_light.setEnabled(False)
            self.ui.kde_combo_dark.setEnabled(False)
            self.ui.kde_checkbox.setChecked(False)
            config.update("codeEnabled", False)

    def get_kde_theme_names(self):
        """
        Returns a map with translations for kde theme names.
        """

        # aliases for path to use later on
        user = pwd.getpwuid(os.getuid())[0]
        path = "/home/" + user + "/.local/share/plasma/look-and-feel/"

        # asks the system what themes are available
        long_names = subprocess.check_output(
            ["lookandfeeltool", "-l"], universal_newlines=True)
        long_names = long_names.splitlines()

        themes = {}

        # get the actual name
        for long in long_names:
            # trying to get the Desktop file
            try:
                # load the name from the metadata.desktop file
                with open('/usr/share/plasma/look-and-feel/{long}/metadata.desktop'.format(**locals()), 'r') as file:
                    # search for the name
                    for line in file:
                        if 'Name=' in line:
                            name: str = ''
                            write: bool = False
                            for letter in line:
                                if letter == '\n':
                                    write = False
                                if write:
                                    name += letter
                                if letter == '=':
                                    write = True
                            themes[name] = long
                            break
            except:
                # check the next path if the themes exist there
                try:
                    # load the name from the metadata.desktop file
                    with open('{path}{long}/metadata.desktop'.format(**locals()), 'r') as file:
                        # search for the name
                        for line in file:
                            if 'Name=' in line:
                                name: str = ''
                                write: bool = False
                                for letter in line:
                                    if letter == '\n':
                                        write = False
                                    if write:
                                        name += letter
                                    if letter == '=':
                                        write = True
                                themes[name] = long
                                break
                        # if no file exist lets just use the long name
                except:
                    themes[long] = long

        return themes

    def get_kde_theme_long(self, short: str):
        """
        Translates short names to long names.
        :param short: short name
        :return: long name
        """
        if short == '' or short is None:
            return
        themes = self.get_kde_theme_names()
        return themes[short]

    def get_kde_theme_short(self, long: str):
        """
        Translates long names to short names.
        :param long: long name
        :return: short name
        """
        if long == '' or long is None:
            return
        themes = self.get_kde_theme_names()
        short_names = list(themes.keys())
        long_names = list(themes.values())
        return short_names[long_names.index(long)]

    def center(self):
        frame_gm = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def toggle_kde_fields(self):
        self.get_kde_themes()
        checked = self.ui.kde_checkbox.isChecked()
        self.ui.kde_combo_light.setEnabled(checked)
        self.ui.kde_combo_dark.setEnabled(checked)
        config.update("codeEnabled", checked)

    def toggle_atom_fields(self):
        checked = self.ui.atom_checkbox.isChecked()
        self.ui.atom_line_light.setEnabled(checked)
        self.ui.atom_line_dark.setEnabled(checked)
        config.update("atomEnabled", checked)

    def toggle_wallpaper_buttons(self):
        checked = self.ui.wallpaper_checkbox.isChecked()
        self.ui.wallpaper_button_light.setEnabled(checked)
        self.ui.wallpaper_button_dark.setEnabled(checked)
        config.update("wallpaperEnabled", checked)

    def toggle_code_fields(self):
        checked = self.ui.code_checkbox.isChecked()
        self.ui.code_line_light.setEnabled(checked)
        self.ui.code_line_dark.setEnabled(checked)
        config.update("codeEnabled", checked)

    def toggle_gtk_fields(self):
        checked = self.ui.gtk_checkbox.isChecked()
        self.ui.gtk_line_light.setEnabled(checked)
        self.ui.gtk_line_dark.setEnabled(checked)
        config.update("gtkEnabled", checked)

    def toggle_kvantum_fields(self):
        checked = self.ui.kvantum_checkbox.isChecked()
        self.ui.kvantum_line_light.setEnabled(checked)
        self.ui.kvantum_line_dark.setEnabled(checked)
        config.update("kvantumEnabled", checked)


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
        if config.is_scheduled():
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
        new_config = config.get_config()
        d_hour = new_config["switchToDark"].split(":")[0]
        d_minute = new_config["switchToDark"].split(":")[1]
        l_hour = new_config["switchToLight"].split(":")[0]
        l_minute = new_config["switchToLight"].split(":")[1]

        # giving the time widget the values of the config
        dark_time = QTime(int(d_hour), int(d_minute))
        light_time = QTime(int(l_hour), int(l_minute))
        self.ui.dark_time.setTime(dark_time)
        self.ui.light_time.setTime(light_time)

    def set_correct_buttons(self):
        theme = config.get_theme()
        if theme == "dark":
            self.ui.light_push.setEnabled(True)
            self.ui.dark_push.setEnabled(False)
        if theme == "light":
            self.ui.light_push.setEnabled(False)
            self.ui.dark_push.setEnabled(True)
        if theme == "":
            self.ui.light_push.setEnabled(True)
            self.ui.dark_push.setEnabled(True)
        self.ui.sound_checkBox.setChecked(config.sound_get_checkbox())

    def time_changed(self):
        # update config if time has changed
        l_hour, l_minute = str(self.ui.light_time.time().hour()), str(
            self.ui.light_time.time().minute())
        d_hour, d_minute = str(self.ui.dark_time.time().hour()), str(
            self.ui.dark_time.time().minute())
        config.update("switchToLight", l_hour + ":" + l_minute)
        config.update("switchToDark", d_hour + ":" + d_minute)

    def toggle_schedule_cliked(self):
        checked = self.ui.schedule_radio.isChecked()
        config.update("schedule", checked)
        if checked:
            self.ui.dark_time.setEnabled(True)
            self.ui.light_time.setEnabled(True)
        else:
            self.ui.dark_time.setEnabled(False)
            self.ui.light_time.setEnabled(False)
