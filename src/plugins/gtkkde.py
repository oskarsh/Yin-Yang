import pwd
import os
import re
from src import config

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


def switchToLight():
    gtk_theme = config.getGtkLightTheme()
    gtk_path = path + "/gtk-3.0"
    with open(gtk_path+"/settings.ini", "r") as file:
        # search for the theme section and change it
        current_theme = re.findall(
            "gtk-theme-name=[A-z -]*", str(file.readlines()))[0][:-2]
        inplace_change(gtk_path+"/settings.ini",
                       current_theme, "gtk-theme-name="+gtk_theme)


def switchToDark():
    gtk_theme = config.getGtkDarkTheme()
    gtk_path = path + "/gtk-3.0"
    with open(gtk_path+"/settings.ini", "r") as file:
        # search for the theme section and change it
        current_theme = re.findall(
            "gtk-theme-name=[A-z -]*", str(file.readlines()))[0][:-2]
        inplace_change(gtk_path+"/settings.ini",
                       current_theme, "gtk-theme-name="+gtk_theme)
