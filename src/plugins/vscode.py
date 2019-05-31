import os
import pwd
import json
from src import config

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config"


def inplace_change(filename, old_string, new_string):
    """@params: config - config to be written into file
               path - the path where the config is will be written into
                defaults to the default path
    """

    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print(
            'Changing "{old_string}" to "{new_string}" in {filename}'
            .format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)


def write_new_settings(settings, path):
    print("SETTINGS ", len(settings))
    # simple adds a new field to the settings
    settings["workbench.colorTheme"] = "Default"
    with open(path, 'w') as conf:
        json.dump(settings, conf, indent=4)


def switch_to_light():
    code_theme = config.get("codeLightTheme")
    possible_editors = [
        path+"/VSCodium/User/settings.json",
        path+"/Code - OSS/User/settings.json",
        path+"/Code/User/settings.json",
        path+"/Code - Insiders/User/settings.json",
    ]

    for editor in possible_editors:
        if os.path.isfile(editor):
            # getting the old theme to replace it
            with open(editor, "r") as sett:
                try:
                    settings = json.load(sett)
                except json.decoder.JSONDecodeError:
                    settings = {}
                    settings["workbench.colorTheme"] = ""
                    write_new_settings(settings, editor)
                try:
                    old_theme = settings["workbench.colorTheme"]
                except KeyError:
                    # happens when the default theme in vscode is
                    print("NO THEME SECTION INSIDE SETTINGS")
                    write_new_settings(settings, editor)
            inplace_change(editor,
                           old_theme, code_theme)


def switch_to_dark():
    code_theme = config.get("codeDarkTheme")
    possible_editors = [
        path+"/VSCodium/User/settings.json",
        path+"/Code - OSS/User/settings.json",
        path+"/Code/User/settings.json",
        path+"/Code - Insiders/User/settings.json",

    ]

    for editor in possible_editors:
        if os.path.isfile(editor):
            # getting the old theme to replace it
            with open(editor, "r") as sett:
                try:
                    settings = json.load(sett)
                except json.decoder.JSONDecodeError:
                    settings = {}
                    settings["workbench.colorTheme"] = ""
                    write_new_settings(settings, editor)
                try:
                    old_theme = settings["workbench.colorTheme"]
                except KeyError:
                    # happens when the default theme in vscode is used
                    write_new_settings(settings, editor)
            inplace_change(editor,
                           old_theme, code_theme)
