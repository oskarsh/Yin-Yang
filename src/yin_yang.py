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
from src import gui
import threading
import time
import pwd
import datetime
import subprocess
from src.plugins import kde, gtkkde, wallpaper, vscode, atom, gtk
from src import config


# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config/"

terminate = False


class Yang(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        if config.get("codeEnabled"):
            vscode.switchToLight()
        if config.get("atomEnabled"):
            atom.switchToLight()
        if config.get("kdeEnabled"):
            kde.switchToLight()
        if config.get("wallpaperEnabled"):
            wallpaper.switchToLight()
        if config.get("gtkEnabled") and config.get("desktop") == "kde":
            gtkkde.switchToLight()
        if config.get("gtkEnabled") and config.get("desktop") == "gtk":
            gtk.switchToLight()
        playSound("./assets/light.wav")


class Yin(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        if config.get("codeEnabled"):
            vscode.switchToDark()

        if config.get("atomEnabled"):
            atom.switchToDark()

        if config.get("kdeEnabled"):
            kde.switchToDark()

        if config.get("wallpaperEnabled"):
            wallpaper.switchToDark()

        # kde support
        if config.get("gtkEnabled") and config.get("desktop") == "kde":
            gtkkde.switchToDark()

        # gnome and budgie support
        if config.get("gtkEnabled") and config.get("desktop") == "gtk":
            gtk.switchToDark()

        playSound("/assets/dark.wav")


class Daemon(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        while(True):

            if terminate:
                config.update("running", False)
                break

            if(not config.isScheduled()):
                config.update("running", False)
                break

            editable = config.getConfig()

            theme = config.get("theme")

            if shouldBeLight():
                if(theme is "light"):
                    time.sleep(30)
                    continue
                else:
                    switchToLight()
            else:
                if(theme is "dark"):
                    time.sleep(30)
                    continue
                else:
                    switchToDark()

            time.sleep(30)


def switchToLight():
    yang = Yang(1)
    yang.start()
    config.update("theme", "light")
    yang.join()


def switchToDark():
    yin = Yin(2)
    yin.start()
    config.update("theme", "dark")
    yin.join()


def startDaemon():
    daemon = Daemon(3)
    daemon.start()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def playSound(sound):
    """ Description - only works with pulseaudio.
    :type sound: String (Path)
    :param sound: Sound path to be played audiofile from
    :rtype: I hope you will hear your Sound ;)
    """


    subprocess.run(["paplay", resource_path(sound)])


def shouldBeLight():
    # desc: return if the Theme should be light
    # returns: True if it should be light
    # returns: False if the theme should be dark

    d_hour = int(config.get("switchToDark").split(":")[0])
    d_minute = int(config.get("switchToDark").split(":")[1])
    l_hour = int(config.get("switchToLight").split(":")[0])
    l_minute = int(config.get("switchToLight").split(":")[1])
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute

    if(hour >= l_hour and hour < d_hour):
        if(hour == l_hour and minute <= l_minute):
            return False
        else:
            return True
    else:
        if(hour == d_hour and minute <= d_minute):
            return True
        else:
            return False
