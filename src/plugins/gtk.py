import subprocess
from src import config


def switchToLight():
    gtk_theme = config.get("gtkLightTheme")
    # gtk_theme = "Default"
    # uses a kde api to switch to a light theme
    subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", gtk_theme])


def switchToDark():
    gtk_theme = config.get("gtkDarkTheme")
    # uses a kde api to switch to a dark theme
    subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", gtk_theme])
