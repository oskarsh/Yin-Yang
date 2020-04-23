import subprocess
from src import config

# WIP: Potential Check  for https://gist.github.com/atiensivu/fcc3183e9a6fd74ec1a283e3b9ad05f0 to reduce common issues, or write it in the FAQ

def switch_to_light():
    gnome_theme = config.get("gnomeLightTheme")
    subprocess.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", '"{}"'.format(gnome_theme)]) # Shell theme


def switch_to_dark():
    gnome_theme = config.get("gnomeDarkTheme")
    subprocess.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", '"{}"'.format(gnome_theme)]) # Shell theme
