import subprocess
from bin import config
import os
import pwd


def switchToDark():

    wallpaper_dark = config.get("wallpaperDarkTheme")

    string = """'string:
    var Desktops = desktops();                                                                                                                       
    for (i=0;i<Desktops.length;i++) {
            d = Desktops[i];
            d.wallpaperPlugin = "org.kde.image";
            d.currentConfigGroup = Array("Wallpaper",
                                        "org.kde.image",
                                        "General");
            d.writeConfig("Image", "file:"""+wallpaper_dark+"""");
    }'"""

    print(string)

    if wallpaper_dark == "":
        subprocess.run(["notify-send", "looks like no dark wallpaper is set"])
    else:
        subprocess.run(["sh", "/opt/yin-yang/bin/change_wallpaper.sh", wallpaper_dark])


def switchToLight():
    wallpaper_light = config.get("wallpaperLightTheme")

    if wallpaper_light == "":
        subprocess.run(["notify-send", "looks like no light wallpaper is set"])
    else:
        subprocess.run(["sh", "/opt/yin-yang/bin/change_wallpaper.sh", wallpaper_light])
