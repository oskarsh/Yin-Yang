import subprocess
from src import config


def switch_to_light():
    gtk_theme = config.get("gtkLightTheme")
    # gtk_theme = "Default"
    # uses a kde api to switch to a light theme
    subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", gtk_theme]) # Applications theme
    subprocess.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", '"{}"'.format(gtk_theme)]) # Shell theme


def switch_to_dark():
    gtk_theme = config.get("gtkDarkTheme")
    # uses a kde api to switch to a dark theme
    subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", gtk_theme]) # Applications theme
    subprocess.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", '"{}"'.format(gtk_theme)]) # Shell theme
