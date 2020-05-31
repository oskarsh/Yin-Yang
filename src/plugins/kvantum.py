import subprocess
from src import config


def switch_to_light():
    kvantum_theme = config.get("kvantumLightTheme")
    # uses a kvantummanager cli to switch to a light theme
    print("LIGHT:", kvantum_theme)
    subprocess.run(["kvantummanager", "--set", kvantum_theme])


def switch_to_dark():
    kvantum_theme = config.get("kvantumDarkTheme")
    # uses a kvantummanager cli to switch to a dark theme
    print("Dark:", kvantum_theme)
    subprocess.run(["kvantummanager", "--set", kvantum_theme])
