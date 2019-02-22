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
    editor = get_editor()
    # updating path for better access
    user_path = path + editor + "/User/"
    settings = user_path + "settings.json"
    yin_path = user_path+"yin.json"

    if (config["theme"] == "light"):
        copyfile(settings, user_path+"tmp_settings")
        copyfile(yin_path, settings)


def switchToDark():
    config = loadConfig()
    editor = get_editor()
    # updating path for better access
    user_path = path + editor + "/User/"
    print(user_path)
    settings = user_path + "settings.json"
    yang_path = user_path+"yang.json"

    if (config["theme"] == "dark"):
        copyfile(settings, user_path+"tmp_settings")
        copyfile(yang_path, settings)


def switchGTKThemeToDark():
    gtk_theme = "Breeze-Dark"
    gtk_path = path + "gtk-3.0/"
    with open(gtk_path+"settings.ini", "r") as file:
        # search for the theme section and change it
        current_theme = re.findall(
            "gtk-theme-name=[A-z -]*", str(file.readlines()))[0][:-2]
        inplace_change(gtk_path+"settings.ini",
                       current_theme, "gtk-theme-name=Breeze-Dark")


def switchGTKThemeToLight():
    gtk_theme = "Breeze"
    gtk_path = path + "gtk-3.0/"
    with open(gtk_path+"settings.ini", "r") as file:
        # search for the theme section and change it
        current_theme = re.findall(
            "gtk-theme-name=[A-z -]*", str(file.readlines()))[0][:-2]
        inplace_change(gtk_path+"settings.ini",
                       current_theme, "gtk-theme-name=Breeze")


def switchKDESettingsToLight():
    subprocess.run(["lookandfeeltool", "-a", "org.kde.breeze.desktop"])


def switchKDEThemeToDark():
    subprocess.run(["lookandfeeltool", "-a", "org.kde.breezedark.desktop"])


#
# @params: config - config to be written into file
#          path - the path where the config is will be written into
#           defaults to the default path
#

def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print(
            'Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)


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


def getActiveTheme(config):
    return config["theme"]


def create_settings_json(path):
    settings = {}
    settings["workbench.colorTheme"] = ""
    with open(path, "w") as setting:
        json.dump(settings, setting)


def get_editor():
    if (os.path.isdir(path+"VSCodium/User/")):
        if (not os.path.isfile(path+"VSCodium/User/settings.json")):
            create_settings_json(path+"VSCodium/User/settings.json")
        editor = "VSCodium"
        return editor

    # check if user is using vscode or vscodium and adapt by setting the editor to it
    if (os.path.isdir(path+"Code - OSS/User/")):
        if (not os.path.isfile(path+"Code - OSS/User/settings.json")):
            create_settings_json(path+"Code - OSS/User/settings.json")
        editor = "Code - OSS"
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
