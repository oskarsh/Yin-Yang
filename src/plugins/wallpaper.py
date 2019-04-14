import subprocess
from src import config
import os
import pwd


def switchToDark():

    wallpaper_dark = config.get("wallpaperDarkTheme")

    if wallpaper_dark == "":
        subprocess.run(["notify-send", "looks like no dark wallpaper is set"])
    else:
        if (config.get("desktop") == "kde"):
            subprocess.run(
                ["sh", "/opt/yin-yang/src/change_wallpaper.sh", wallpaper_dark])
        if (config.get("desktop") == "gtk"):
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background",
                            "picture-uri", "file://"+wallpaper_dark])


def switchToLight():
    wallpaper_light = config.get("wallpaperLightTheme")

    if wallpaper_light == "":
        subprocess.run(["notify-send", "looks like no light wallpaper is set"])
    else:
        if (config.get("desktop") == "kde"):
            subprocess.run(
                ["sh", "/opt/yin-yang/src/change_wallpaper.sh", wallpaper_light])
        if (config.get("desktop") == "gtk"):
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background",
                            "picture-uri", "file://"+wallpaper_light])
