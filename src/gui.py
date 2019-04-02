
import subprocess
import re
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
        # center the settingswindow
        self.center()
        # syncing with config - fill out all fields based on Config
        self.syncWithConfig()
        # register all the handler onClick functions ...
        self.registerHandlers()

    def closeEvent(self, event):
        # overwrites the function that gets called when window is closed
        self.saveAndExit()

    def saveAndExit(self):
        print("saving options")

        config.update("kdeLightTheme", self.ui.kde_combo_light.currentText())
        config.update("kdeDarkTheme", self.ui.kde_combo_dark.currentText())
        config.update("kdeEnabled", self.ui.kde_checkbox.isChecked())

        config.update("codeLightTheme", self.ui.code_line_light.text())
        config.update("codeDarkTheme", self.ui.code_line_dark.text())
        config.update("codeEnabled", self.ui.code_checkbox.isChecked())

        config.update("gtkLightTheme", self.ui.gtk_line_light.text())
        config.update("gtkDarkTheme", self.ui.gtk_line_dark.text())
        config.update("gtkEnabled", self.ui.gtk_checkbox.isChecked())

        config.update("atomLightTheme", self.ui.atom_line_light.text())
        config.update("atomDarkTheme", self.ui.atom_line_dark.text())
        config.update("atomEnabled", self.ui.atom_checkbox.isChecked())

        # showing the main window and hiding the current one
        self.hide()
        self.window = MainWindow()
        self.window.show()

    def registerHandlers(self):
        self.ui.kde_checkbox.toggled.connect(self.toggleKdeFields)
        self.ui.code_checkbox.toggled.connect(self.toggleCodeFields)
        self.ui.gtk_checkbox.toggled.connect(self.toggleGtkFields)
        self.ui.atom_checkbox.toggled.connect(self.toggleAtomFields)
        self.ui.wallpaper_button_light.clicked.connect(self.openWallpaperLight)
        self.ui.wallpaper_button_dark.clicked.connect(self.openWallpaperDark)
        self.ui.wallpaper_checkbox.toggled.connect(self.toggleWallpaperButtons)
        self.ui.back_button.clicked.connect(self.saveAndExit)

    def syncWithConfig(self):
        # sync config label with get the correct version
        self.ui.version_label.setText("yin-yang: v" + config.getVersion())
        # syncing all fields and checkboxes with config
        # ---- KDE -----
        # reads out all kde themes and displays them inside a combobox
        if (config.get("kdeEnabled")):
            # if (self.ui.kde_combo_light.count())
            print(self.ui.kde_combo_dark.count())
            # fixed bug where themes get appended multiple times
            self.getKdeThemes()

            self.ui.kde_checkbox.setChecked(config.get("kdeEnabled"))
            self.ui.kde_combo_dark.setEnabled(config.get("kdeEnabled"))
            self.ui.kde_combo_light.setEnabled(config.get("kdeEnabled"))
            index_light = self.ui.kde_combo_light.findText(
                config.get("kdeLightTheme"))
            self.ui.kde_combo_light.setCurrentIndex(index_light)
            index_dark = self.ui.kde_combo_dark.findText(
                config.get("kdeDarkTheme"))
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

    def openWallpaperLight(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Wallpaper Light", "")
        subprocess.run(["notify-send", "Light Wallpaper set"])
        config.update("wallpaperLightTheme", fileName)

    def openWallpaperDark(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Wallpaper Dark", "")
        subprocess.run(["notify-send", "Dark Wallpaper set"])
        config.update("wallpaperDarkTheme", fileName)

    def getKdeThemes(self):
        if (config.get("desktop") == "kde"):
            if (self.ui.kde_combo_light.count() == 0 and self.ui.kde_combo_dark.count() == 0):
                # asks the system what themes are available
                ugly_themes = subprocess.check_output(
                    ["lookandfeeltool", "-l"])
                print(ugly_themes)
                pretty_themes = re.findall(
                    "[b]?[']?n?([A-z]*.[A-z]*.[A-z]*-?.[A-z]*.[A-z]*)\\\\", str(ugly_themes))
                for theme in pretty_themes:
                    self.ui.kde_combo_light.addItem(theme)
                    self.ui.kde_combo_dark.addItem(theme)
        else:
            subprocess.run(
                ["notify-send", "It looks like you are not running KDE"])

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def toggleKdeFields(self):
        self.getKdeThemes()
        checked = self.ui.kde_checkbox.isChecked()
        self.ui.kde_combo_light.setEnabled(checked)
        self.ui.kde_combo_dark.setEnabled(checked)
        config.update("codeEnabled", checked)

    def toggleAtomFields(self):
        checked = self.ui.atom_checkbox.isChecked()
        self.ui.atom_line_light.setEnabled(checked)
        self.ui.atom_line_dark.setEnabled(checked)
        config.update("atomEnabled", checked)

    def toggleWallpaperButtons(self):
        checked = self.ui.wallpaper_checkbox.isChecked()
        self.ui.wallpaper_button_light.setEnabled(checked)
        self.ui.wallpaper_button_dark.setEnabled(checked)
        config.update("wallpaperEnabled", checked)

    def toggleCodeFields(self):
        checked = self.ui.code_checkbox.isChecked()
        self.ui.code_line_light.setEnabled(checked)
        self.ui.code_line_dark.setEnabled(checked)
        config.update("codeEnabled", checked)

    def toggleGtkFields(self):
        checked = self.ui.gtk_checkbox.isChecked()
        self.ui.gtk_line_light.setEnabled(checked)
        self.ui.gtk_line_dark.setEnabled(checked)
        config.update("gtkEnabled", checked)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yin-Yang")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # center itself
        self.center()
        # connects all buttons to the correct routes
        self.registerHandlers()
        # syncs the UI with the config
        self.syncWithConfig()

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def registerHandlers(self):
        # connect the "light" button
        self.ui.light_push.clicked.connect(self.toggleLight)
        # connect the "dark" button
        self.ui.dark_push.clicked.connect(self.toggleDark)
        # connect the settingsButton
        self.ui.settings_push.clicked.connect(self.openSettings)
        # connect the time change with the correct function
        self.ui.light_time.timeChanged.connect(self.timeChanged)
        self.ui.dark_time.timeChanged.connect(self.timeChanged)
        self.ui.schedule_radio.toggled.connect(self.toggleScheduleClicked)

    def syncWithConfig(self):
        # sets the scheduled button to be enabled or disabled
        if (config.isScheduled()):
            self.ui.schedule_radio.setChecked(True)
            self.ui.dark_time.setEnabled(True)
            self.ui.light_time.setEnabled(True)
            yin_yang.startDaemon()
        # sets the correct time based on config
        self.setCorrectTime()
        # setting the correct buttons based on config "dark"  "light"
        self.setCorrectButtons()

    def openSettings(self):
        self.secwindow = SettingsWindow()
        self.secwindow.setWindowTitle("Settings")
        self.secwindow.show()
        self.hide()

    def toggleLight(self):
        yin_yang.switchToLight()
        self.syncWithConfig()
        # experimental
        # self.restart()

    def toggleDark(self):
        yin_yang.switchToDark()
        self.syncWithConfig()
        # self.restart()

    # no needed since QT is now used system wise instead of python wise
    # def restart(self):
    #     """Restarts the current program.
    #     Note: this function does not return. Any cleanup action (like
    #     saving data) must be done before calling this function."""
    #     python = sys.executable
    #     os.execl(python, python, * sys.argv)

    def setCorrectTime(self):
        new_config = config.getConfig()
        d_hour = new_config["switchToDark"].split(":")[0]
        d_minute = new_config["switchToDark"].split(":")[1]
        l_hour = new_config["switchToLight"].split(":")[0]
        l_minute = new_config["switchToLight"].split(":")[1]

        # giving the time widget the values of the config
        dark_time = QTime(int(d_hour), int(d_minute))
        light_time = QTime(int(l_hour), int(l_minute))
        self.ui.dark_time.setTime(dark_time)
        self.ui.light_time.setTime(light_time)

    def setCorrectButtons(self):
        theme = config.getTheme()
        if (theme == "dark"):
            self.ui.light_push.setEnabled(True)
            self.ui.dark_push.setEnabled(False)
        if (theme == "light"):
            self.ui.light_push.setEnabled(False)
            self.ui.dark_push.setEnabled(True)
        if (theme == ""):
            self.ui.light_push.setEnabled(True)
            self.ui.dark_push.setEnabled(True)

    def timeChanged(self):
        # update config if time has changed
        l_hour, l_minute = str(self.ui.light_time.time().hour()), str(
            self.ui.light_time.time().minute())
        d_hour, d_minute = str(self.ui.dark_time.time().hour()), str(
            self.ui.dark_time.time().minute())
        config.update("switchToLight", l_hour + ":" + l_minute)
        config.update("switchToDark", d_hour + ":" + d_minute)

    def toggleScheduleClicked(self):
        checked = self.ui.schedule_radio.isChecked()
        config.update("schedule", checked)
        if(checked):
            self.ui.dark_time.setEnabled(True)
            self.ui.light_time.setEnabled(True)
        else:
            self.ui.dark_time.setEnabled(False)
            self.ui.light_time.setEnabled(False)
