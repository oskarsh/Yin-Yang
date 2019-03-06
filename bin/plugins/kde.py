import subprocess
from bin import config


def switchToLight():
    kde_theme = config.getKdeLightTheme()
    # uses a kde api to switch to a light theme
    print(kde_theme)
    subprocess.run(["lookandfeeltool", "-a", kde_theme])


def switchToDark():

    kde_theme = config.getKdeDarkTheme()
    # uses a kde api to switch to a dark theme
    print(kde_theme)
    subprocess.run(["lookandfeeltool", "-a", kde_theme])
