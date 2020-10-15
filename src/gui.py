import subprocess
import pwd
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog
from src.ui.mainwindow import Ui_MainWindow
from src.ui.settings import Ui_PluginWindow as Ui_SettingsWindow
from src import yin_yang
from src import config


class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        # center the settingswindow
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
        config.update("kdeEnabled", self.ui.groupKde.isChecked())

        config.update("gnomeEnabled", self.ui.groupGnome.isChecked())
        config.update("gnomeLightTheme", self.ui.gnome_lineEdit_light.text())
        config.update("gnomeDarkTheme", self.ui.gnome_lineEdit_dark.text())

        config.update("gtkLightTheme", self.ui.gtk_line_light.text())
        config.update("gtkDarkTheme", self.ui.gtk_line_dark.text())
        config.update("gtkEnabled", self.ui.groupGtk.isChecked())

        config.update("firefoxEnabled", self.ui.groupFirefox.isChecked())
        config.update("firefoxDarkTheme", self.ui.groupFirefox.line_dark.text())
        config.update("firefoxLightTheme", self.ui.groupFirefox.line_light.text())

        config.update("codeLightTheme", self.ui.code_line_light.text())
        config.update("codeDarkTheme", self.ui.code_line_dark.text())
        config.update("codeEnabled", self.ui.groupVscode.isChecked())

        config.update("atomLightTheme", self.ui.atom_line_light.text())
        config.update("atomDarkTheme", self.ui.atom_line_dark.text())
        config.update("atomEnabled", self.ui.groupAtom.isChecked())

        # showing the main window and hiding the current one
        self.hide()
        self.window = MainWindow()
        self.window.show()

    def register_handlers(self):
        self.ui.wallpaper_button_light.clicked.connect(
            self.open_wallpaper_light)
        self.ui.wallpaper_button_dark.clicked.connect(self.open_wallpaper_dark)
        self.ui.back_button.clicked.connect(self.save_and_exit)
        self.ui.checkSound.clicked.connect(self.toggle_sound())

    def sync_with_config(self):
        # sync config label with get the correct version
        self.ui.statusBar.currentMessage("yin-yang: v" + config.get_version())
        # syncing all fields and checkboxes with config
        # ---- KDE -----
        # reads out all kde themes and displays them inside a combobox
        if config.get("kdeEnabled"):
            # fixed bug where themes get appended multiple times
            self.get_kde_themes()

            self.ui.groupKde.setChecked(config.get("kdeEnabled"))
            index_light = self.ui.kde_combo_light.findText(
                self.get_kde_theme_short(config.get("kdeLightTheme")))
            self.ui.kde_combo_light.setCurrentIndex(index_light)
            index_dark = self.ui.kde_combo_dark.findText(
                self.get_kde_theme_short(config.get("kdeDarkTheme")))
            self.ui.kde_combo_dark.setCurrentIndex(index_dark)
        # ---- VSCode ----
        self.ui.code_line_light.setText(config.get("codeLightTheme"))
        self.ui.code_line_dark.setText(config.get("codeDarkTheme"))
        self.ui.groupCode.setChecked(config.get("codeEnabled"))
        # ---- GTK -----
        self.ui.gtk_line_light.setText(config.get("gtkLightTheme"))
        self.ui.gtk_line_dark.setText(config.get("gtkDarkTheme"))
        self.ui.grouGtk.setChecked(config.get("gtkEnabled"))
        # ----- wallpaper --------
        self.ui.groupWallpaper.setChecked(config.get("wallpaperEnabled"))
        # ----- Atom --------
        self.ui.atom_line_light.setText(config.get("atomLightTheme"))
        self.ui.atom_line_dark.setText(config.get("atomDarkTheme"))
        self.ui.groupAtom.setChecked(config.get("atomEnabled"))

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
            self.ui.groupKde.setChecked(False)
            config.update("kdeEnabled", False)

    def get_kde_theme_names(self):
        """
        Returns a map with translations for kde theme names.
        """

        # aliases for path to use later on
        user = pwd.getpwuid(os.getuid())[0]
        path = "/home/"+user+"/.local/share/plasma/look-and-feel/"

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
        self.ui.buttonLight.clicked.connect(self.toggle_light)
        # connect the "dark" button
        self.ui.buttonDark.clicked.connect(self.toggle_dark)
        # connect the settingsButton
        self.ui.buttonApplication.clicked.connect(self.open_settings)
        # connect the time change with the correct function
        self.ui.inTimeLight.timeChanged.connect(self.time_changed)
        self.ui.inTimeDark.timeChanged.connect(self.time_changed)
        self.ui.buttonSchedule.toggled.connect(self.toggle_schedule_cliked)

    def sync_with_config(self):
        # sets the scheduled button to be enabled or disabled
        if config.get("schedule"):
            if config.get("followSun"):
                self.ui.buttonSun.setChecked(True)
            else:
                self.ui.buttonSchedule.setChecked(True)
            yin_yang.start_daemon()
        else:
            self.ui.automatic.setChecked(False)

        # sets the correct time based on config
        self.set_correct_time()
        # enable the correct button based on config
        self.set_correct_buttons()
        # connect checkbox for sound with config
        if config.get("soundEnabled"):
            self.ui.checkSound.setChecked()

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
        config.update("soundEnabled", self.ui.checkSound.isChecked())
        self.sync_with_config()

    # no needed since QT is now used system wise instead of python wise
    def restart(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def set_correct_time(self):
        new_config = config.get_config()
        d_hour = new_config["switchToDark"].split(":")[0]
        d_minute = new_config["switchToDark"].split(":")[1]
        l_hour = new_config["switchToLight"].split(":")[0]
        l_minute = new_config["switchToLight"].split(":")[1]

        # giving the time widget the values of the config
        dark_time = QTime(int(d_hour), int(d_minute))
        light_time = QTime(int(l_hour), int(l_minute))
        self.ui.inTimeDark.setTime(dark_time)
        self.ui.inTimeLight.setTime(light_time)

    def set_correct_buttons(self):
        theme = config.get_theme()
        if theme == "dark":
            self.ui.buttonLight.setEnabled(False)
        if theme == "light":
            self.ui.buttonDark.setEnabled(False)

    def time_changed(self):
        # update config if time has changed
        l_hour, l_minute = str(self.ui.inTimeLight.time().hour()), str(
            self.ui.inTimeLight.time().minute())
        d_hour, d_minute = str(self.ui.inTimeDark.time().hour()), str(
            self.ui.inTimeDark.time().minute())
        config.update("switchToLight", l_hour + ":" + l_minute)
        config.update("switchToDark", d_hour + ":" + d_minute)

    def toggle_schedule_cliked(self):
        checked = self.ui.buttonSchedule.isChecked()
        config.update("schedule", checked)
