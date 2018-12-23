#!/bin/python


#
# title: yin_yang
# description: yin_yang provides a easy way to toggle between light and dark mode for your kde desktop. It also themes your vscode and all other qt application with it.
# author: daehruoydeef
# date: 21.12.2018
# license: MIT
#

import os
import sys
import json
import pathlib
import pwd
import time
import datetime
import subprocess
from argparse import ArgumentParser
import re
from shutil import copyfile, move

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config/"

def create_yin(yin_path):
    with open(yin_path, "r") as yin:
        data = json.load(yin)

    with open(yin_path, "w") as yin:
        data["workbench.colorTheme"] = "Default Light+"
        json.dump(data, yin)

    return data

def create_yang(yang_path):

    with open(yang_path, "r") as yang:
        data = json.load(yang)

    with open(yang_path, "w") as yang:
        data["workbench.colorTheme"] = "Default Dark+"
        json.dump(data, yang)

    return data

def create_yin_yang(editor):
    user = pwd.getpwuid(os.getuid())[0]
    path = "/home/"+user+"/.config/"+editor+"/User/"
    settings = path + "settings.json"
    yin_path = path + "yin.json"
    yang_path = path + "yang.json"

    # creating copies of the settings
    copyfile(settings, yin_path)
    copyfile(settings, yang_path)

    # adjust theme inside those settings to
    # match the dark or light theme
    create_yin(yin_path)
    create_yang(yang_path)

def switchToLight():
    config = loadConfig()
    editor = getEditor(config)
    # updating path for better access
    user_path = path + editor + "/User/"
    settings = user_path + "settings.json"
    yin_path = user_path+"yin.json"

    if (config["theme"] == "light"):
        copyfile(settings, user_path+"tmp_settings")
        copyfile(yin_path, settings)

def switchToDark():
    config = loadConfig()
    editor = getEditor(config)
    # updating path for better access
    user_path = path + editor + "/User/"
    settings = user_path + "settings.json"
    yang_path = user_path+"yang.json"

    if (config["theme"] == "dark"):
        copyfile(settings, user_path+"tmp_settings")
        copyfile(yang_path, settings)

def switchKDESettingsToLight():
    subprocess.run(["lookandfeeltool", "-a", "org.kde.breeze.desktop"])

def switchKDEThemeToDark():
    subprocess.run(["lookandfeeltool", "-a", "org.kde.breezedark.desktop"])


#
# @params: config - config to be written into file
#          path - the path where the config is will be written into
#           defaults to the default path
#


def writeConfig(config):

    # aliases for path to use later on
    user = pwd.getpwuid(os.getuid())[0]
    path = "/home/"+user+"/.config/yin_yang"

    with open(path+"/yin_yang.json", 'w') as conf:
        json.dump(config, conf, indent=4)


def updateConfig(type, item):
    config = loadConfig()
    config[type] = item
    writeConfig(config)

# @params: config - the config where the theme will be extracted from
# @returns : the theme which is currently in use
#
def getActiveTheme(config):
    return config["theme"]


def getEditor(config):
    # check if user is using vscode or vscodium and adapt by setting the editor to it
    if (os.path.isfile(path+"Code - OSS/User/settings.json")):
        editor = "Code - OSS"
        return editor

    if (os.path.isfile(path+"VSCodium/User/settings.json")):
        editor = "VSCodium"
        return editor

    return ""


def loadConfig():

    # aliases for path to use later on
    user = pwd.getpwuid(os.getuid())[0]
    path = "/home/"+user+"/.config/yin_yang"

    with open(path+"/yin_yang.json", "r") as conf:
        config = json.load(conf)
    return config


def configExists():

    # aliases for path to use later on
    user = pwd.getpwuid(os.getuid())[0]
    path = "/home/"+user+"/.config/yin_yang"

    return os.path.isfile(path+"/yin_yang.json")


def createDefaultConfig():

    # aliases for path to use later on
    user = pwd.getpwuid(os.getuid())[0]
    path = "/home/"+user+"/.config/yin_yang"

    # creating the yin yang folder inside config
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    # create empty config as json object
    config = {}

    # fill with default values
    config["version"] = "0.1"
    config["theme"] = ""
    config["codeTheme"] = ""
    config["editor"] = ""
    config["kdeTheme"] = ""
    config["schedule"] = False
    config["switchToDark"] = "20:00"
    config["switchToLight"] = "07:00"
    config["running"] = False
    writeConfig(config)
    return config
