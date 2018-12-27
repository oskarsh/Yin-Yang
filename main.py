import sys
import os
import subprocess
import threading
import signal
from datetime import datetime
from qtpy import QtWidgets
from PyQt5.QtCore import QTime
from bin.ui.mainwindow import Ui_MainWindow
from bin.yin_yang import *

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
ui_window = Ui_MainWindow()
ui_window.setupUi(window)

terminate = False


class Listener(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("background listener started")
        while(True):

            if terminate:
                updateConfig("running", False)
                break

            config = loadConfig()

            if(not config["schedule"]):
                updateConfig("running", False)
                break

            d_hour = config["switchToDark"].split(":")[0]
            d_minute = config["switchToDark"].split(":")[1]
            l_hour = config["switchToLight"].split(":")[0]
            l_minute = config["switchToLight"].split(":")[1]
            hour = datetime.datetime.now().time().hour
            minute = datetime.datetime.now().time().minute

            if (hour == int(d_hour) and minute == int(d_minute)):
                toggleDark()
                time.sleep(61)
            if (hour == int(l_hour) and minute == int(l_minute)):
                toggleLight()
                time.sleep(61)
            time.sleep(1)


class Yin(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):

        updateConfig("theme", "dark")
        config = loadConfig()
        if(config["editor"] != ""):
            switchToDark()
        switchKDEThemeToDark()


class Yang(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        updateConfig("theme", "light")
        config = loadConfig()
        if(config["editor"] != ""):
            switchToLight()
        switchKDESettingsToLight()


def enableCorrectButton(theme):
    if (theme == "dark"):
        ui_window.light_push.setEnabled(True)
        ui_window.dark_push.setEnabled(False)
    if (theme == "light"):
        ui_window.light_push.setEnabled(False)
        ui_window.dark_push.setEnabled(True)
    if (theme == ""):
        ui_window.light_push.setEnabled(True)
        ui_window.dark_push.setEnabled(True)


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


def clickLight():
    toggleLight()
    time.sleep(1)
    restart_program()


def toggleLight():
    thread1 = Yang(1, "Thread-Light")
    thread1.start()
    ui_window.light_push.setEnabled(False)
    ui_window.dark_push.setEnabled(True)


def clickDark():
    toggleDark()
    time.sleep(1)
    restart_program()


def toggleDark():
    thread1 = Yin(2, "Thread-Dark")
    thread1.start()
    ui_window.light_push.setEnabled(True)
    ui_window.dark_push.setEnabled(False)


def isScheduled(config):
    if (config["schedule"]):
        return True
    else:
        return False


def toggleScheduleClicked():
    checked = ui_window.schedule_radio.isChecked()
    updateConfig("schedule", checked)
    if(checked):
        ui_window.dark_time.setEnabled(True)
        ui_window.light_time.setEnabled(True)
        startListener()

    else:
        ui_window.dark_time.setEnabled(False)
        ui_window.light_time.setEnabled(False)


def setCorrectTime():
    config = loadConfig()
    d_hour = config["switchToDark"].split(":")[0]
    d_minute = config["switchToDark"].split(":")[1]
    l_hour = config["switchToLight"].split(":")[0]
    l_minute = config["switchToLight"].split(":")[1]

    # giving the time widget the values of the config
    dark_time = QTime(int(d_hour), int(d_minute))
    light_time = QTime(int(l_hour), int(l_minute))
    ui_window.dark_time.setTime(dark_time)
    ui_window.light_time.setTime(light_time)


def timeChanged():
    l_hour, l_minute = str(ui_window.light_time.time().hour()), str(
        ui_window.light_time.time().minute())
    d_hour, d_minute = str(ui_window.dark_time.time().hour()), str(
        ui_window.dark_time.time().minute())
    updateConfig("switchToLight", l_hour + ":" + l_minute)
    updateConfig("switchToDark", d_hour + ":" + d_minute)


def startListener():
    config = loadConfig()
    # check if scheduled time is checked
    # if it is checked keep listener to wait for correct time
    # open thread and keep listening
    if (not config["running"]):
        updateConfig("running", True)
        listener = Listener(3, "Thread-Listener")
        listener.start()


def signal_handling(signum, frame):
    global terminate
    terminate = True


def center():
    frameGm = window.frameGeometry()
    centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())

def swapTheme(theme):
    if (theme == "dark"):
        toggleLight()
    else:
        toggleDark()

def main():

    parser = ArgumentParser()
    parser.add_argument("-gui", "--gui",
                        help="opens Yin-Yang as a GUI application",
                        action="store_true")
    parser.add_argument("-s", "--schedule",
                    help="starts automatic theme change on time specified inside gui",
                    action="store_true")                   

    args = parser.parse_args()

    # getting user editor
    editor = get_editor()
    if (editor == "VSCodium" or editor == "Code - OSS"):
        updateConfig("editor", editor)
        # creating light and dark version of settings
        create_yin_yang(editor)

    # if no config exists create one with default values
    # else read the current config
    if (not configExists()):
        config = createDefaultConfig()
    else:
        config = loadConfig()

    theme = getActiveTheme(config)
    if (len(sys.argv) == 1 and not args.gui):
        swapTheme(theme)
   
    if (args.schedule):
        updateConfig("running", False)
        startListener()

    if (args.gui):
        # centerin application
        center()

        # enabling the correct buttons
        enableCorrectButton(theme)

        # connecting button handlers
        ui_window.light_push.clicked.connect(clickLight)
        ui_window.dark_push.clicked.connect(clickDark)
        setCorrectTime()
        # setting the radio button and updating it
        ui_window.schedule_radio.setChecked(isScheduled(config))
        ui_window.schedule_radio.toggled.connect(toggleScheduleClicked)
        if(ui_window.schedule_radio.isChecked()):
            ui_window.dark_time.setEnabled(True)
            ui_window.light_time.setEnabled(True)
            updateConfig("running", False)
            startListener()

        # writing config on time change
        ui_window.light_time.timeChanged.connect(timeChanged)
        ui_window.dark_time.timeChanged.connect(timeChanged)

        signal.signal(signal.SIGINT, signal_handling)

        window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
