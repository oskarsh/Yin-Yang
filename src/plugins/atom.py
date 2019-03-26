from src import config
import os
import pwd
import json

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config"


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


def switchToLight():
    pass


def switchToDark():
    pass