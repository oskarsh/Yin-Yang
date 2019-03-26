import subprocess
from src import config


def switchToLight():
    kde_theme = config.get("kdeLightTheme")
    # uses a kde api to switch to a light theme
    print("LIGHT:", kde_theme)
    subprocess.run(["lookandfeeltool", "-a", kde_theme])


def switchToDark():

    kde_theme = config.get("kdeDarkTheme")
    # uses a kde api to switch to a dark theme
    print("Dark:", kde_theme)
    subprocess.run(["lookandfeeltool", "-a", kde_theme])
