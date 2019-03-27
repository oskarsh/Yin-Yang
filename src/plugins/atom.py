from src import config
import os
import pwd
import json
import re

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.atom/"


def inplace_change(filename, old_string, new_string):
    #
    # @params: config - config to be written into file
    #          path - the path where the config is will be written into
    #           defaults to the default path

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


def writeNewSettings(settings, path):
    print("SETTINGS ", len(settings))
    # simple adds a new field to the settings
    settings["workbench.colorTheme"] = "Default"
    with open(path, 'w') as conf:
        json.dump(settings, conf, indent=4)

def getOldTheme(settings):
  # returns the theme which is currently used
  # uses regex to find the currently used theme
  # i excpect that themes follow this pattern
  # XXXX-XXXX-ui     XXXX-XXXX-syntax
  with open (settings, "r") as file:
    string = file.read()
    # themes = re.findall(r'themes: \[[\s]*"([A-Za-z0-9\-]*)"[\s]*"([A-Za-z0-9\-]*)"', string)
    themes = re.findall(r'themes: \[[\s]*"([A-Za-z0-9\-]*)"[\s]*"([A-Za-z0-9\-]*)"', string)
    if len(themes) >= 1:
      uiTheme, syntaxTheme = themes[0]
      usedTheme = re.findall("([A-z\-A-z]*)\-", uiTheme)[0]
      print(usedTheme)
      return usedTheme
    
def switchToLight():
    # get theme out of config
    atomTheme = config.get("atomLightTheme")

    # getting the old theme first
    currentTheme = getOldTheme(path+"config.cson")

    # updating the old theme with theme specfied in config
    inplace_change(path+"config.cson", currentTheme, atomTheme)


def switchToDark():
    # get theme out of config
    atomTheme = config.get("atomDarkTheme")

    # getting the old theme first
    currentTheme = getOldTheme(path+"config.cson")

    # updating the old theme with theme specfied in config
    inplace_change(path+"config.cson", currentTheme, atomTheme)