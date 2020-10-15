import os
import pwd
import json
import re
from src import config

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.atom/"


def inplace_change(filename, old_string, new_string):
    """@params: config - config to be written into file
                path - the path where the config is will be written into.
                    Defaults to the default path
    """
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
    # write the changed content, if found in the file
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

def get_old_theme(settings):
    """returns the theme which is currently used
       uses regex to find the currently used theme
       i excpect that themes follow this pattern
       XXXX-XXXX-ui     XXXX-XXXX-syntax
    """
    with open(settings, "r") as file:
        string = file.read()
        # themes = findall(themes: [ anyword anword])
        themes = re.findall(r'themes: \[[\s]*"([A-Za-z0-9\-]*)"[\s]*"([A-Za-z0-9\-]*)"', string)
        if len(themes) == 0:
            # setting defaut value for themes
            themes = [["one-dark-ui", "one-dark-syntax"]]
        if len(themes) >= 1:
            ui_theme, syntax_theme = themes[0]
            used_theme = re.findall("([A-z\-A-z]*)\-", ui_theme)[0]
            print(used_theme)
            return used_theme

def switch_to_light():
    # get theme out of config
    atom_theme = config.get("atomLightTheme")

    # getting the old theme first
    current_theme = get_old_theme(path+"config.cson")

    # check if already used
    if atom_theme != current_theme:
        # updating the old theme with theme specfied in config
        inplace_change(path+"config.cson", current_theme, atom_theme)


def switch_to_dark():
    # get theme out of config
    atom_theme = config.get("atomDarkTheme")

    # getting the old theme first
    current_theme = get_old_theme(path+"config.cson")

    # check if already used
    if atom_theme != current_theme:
        # updating the old theme with theme specfied in config
        inplace_change(path+"config.cson", current_theme, atom_theme)
