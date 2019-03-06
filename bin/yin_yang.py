#!/bin/python


#
# title: yin_yang
# description: yin_yang provides a easy way to toggle between light and dark
# mode for your kde desktop. It also themes your vscode and
# all other qt application with it.
# author: daehruoydeef
# date: 21.12.2018
# license: MIT
#

import os
import sys
import threading
import time
import pwd
import datetime
import subprocess
from bin.plugins import kde, gtk, wallpaper
from bin import config


# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config/"

terminate = False


class Yang(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        kde.switchToLight()
        wallpaper.switchToLight()
        # gtk.switchToLight()


class Yin(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        kde.switchToDark()
        wallpaper.switchToDark()
        # gtk.switchToDark()
        playSound()


class Daemon(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("background listener started")
        while(True):

            if terminate:
                config.update("running", False)
                break

            if(not config.isScheduled()):
                config.update("running", False)
                break

            editable = config.getConfig()

            d_hour = editable["switchToDark"].split(":")[0]
            d_minute = editable["switchToDark"].split(":")[1]
            l_hour = editable["switchToLight"].split(":")[0]
            l_minute = editable["switchToLight"].split(":")[1]
            hour = datetime.datetime.now().time().hour
            minute = datetime.datetime.now().time().minute

            if (hour == int(d_hour) and minute == int(d_minute)):
                switchToDark()
                time.sleep(61)
            if (hour == int(l_hour) and minute == int(l_minute)):
                switchToLight()
                time.sleep(61)
            time.sleep(1)


def switchToLight():
    yang = Yang(1)
    yang.start()
    config.update("theme", "light")


def switchToDark():
    yin = Yin(2)
    yin.start()
    config.update("theme", "dark")


def startDaemon():
    daemon = Daemon(3)
    daemon.start()


def restart():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


def playSound():
    """ Description - only works with pulseaudio.
    :type sound: String (Path)
    :param sound: Sound path to be played audiofile from
    :rtype: I hope you will hear your Sound ;)
    """
    sound = "./assets/sound.mp3"
    subprocess.run(["paplay", sound])
