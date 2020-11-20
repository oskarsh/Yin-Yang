import json
import os
import pathlib
import re

from main import assembly_version
from suntime import Sun, SunTimeException

# aliases for path to use later on
home = os.getenv("HOME")
path = home + "/.config"


def exists():
    """returns True or False whether Config exists"""
    return os.path.isfile(path + "/yin_yang/yin_yang.json")


def get_desktop():
    """Return the current desktops name or 'unknown' if can't determine it"""
    # just to get all possible implementations of desktop variables
    env = str(os.getenv("GDMSESSION")).lower()
    second_env = str(os.getenv("XDG_CURRENT_DESKTOP")).lower()
    third_env = str(os.getenv("XDG_CURRENT_DESKTOP")).lower()

    # these are the envs I will look for
    # feel free to add your Desktop and see if it works
    gnome_re = re.compile(r'gnome')
    budgie_re = re.compile(r'budgie')
    kde_re = re.compile(r'kde')
    plasma_re = re.compile(r'plasma')
    plasma5_re = re.compile(r'plasma5')

    if gnome_re.search(env) or gnome_re.search(second_env) or gnome_re.search(third_env):
        return "gtk"
    if budgie_re.search(env) or budgie_re.search(second_env) or budgie_re.search(third_env):
        return "gtk"
    if kde_re.search(env) or kde_re.search(second_env) or kde_re.search(third_env):
        return "kde"
    if plasma_re.search(env) or plasma_re.search(second_env) or plasma_re.search(third_env):
        return "kde"
    if plasma5_re.search(env) or plasma5_re.search(second_env) or plasma5_re.search(third_env):
        return "kde"
    return "unknown"


def set_sun_time():
    latitude: float = float(get("latitude"))
    longitude: float = float(get("longitude"))
    sun = Sun(latitude, longitude)

    try:
        today_sr = sun.get_local_sunrise_time()
        today_ss = sun.get_local_sunset_time()

        print('Today the sun raised at {} and get down at {}'.
              format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

        # Get today's sunrise and sunset in UTC
        update("switchToLight", today_sr.strftime('%H:%M'))
        update("switchToDark", today_ss.strftime('%H:%M'))

    except SunTimeException as e:
        print("Error: {0}.".format(e))


# generate path for yin-yang if there is none this will be skipped
pathlib.Path(path + "/yin_yang").mkdir(parents=True, exist_ok=True)

# if there is no config generate a generic one
config = {}
config["version"] = assembly_version
config["desktop"] = get_desktop()
config["followSun"] = False
config["latitude"] = ""
config["longitude"] = ""
config["schedule"] = False
config["switchToDark"] = "20:00"
config["switchToLight"] = "07:00"
config["running"] = False
config["theme"] = ""
config["codeLightTheme"] = "Default Light+"
config["codeDarkTheme"] = "Default Dark+"
config["codeEnabled"] = False
config["kdeLightTheme"] = "org.kde.breeze.desktop"
config["kdeDarkTheme"] = "org.kde.breezedark.desktop"
config["kdeEnabled"] = False
config["gtkLightTheme"] = ""
config["gtkDarkTheme"] = ""
config["atomLightTheme"] = ""
config["atomDarkTheme"] = ""
config["atomEnabled"] = False
config["gtkEnabled"] = False
config["wallpaperLightTheme"] = ""
config["wallpaperDarkTheme"] = ""
config["wallpaperEnabled"] = False
config["firefoxEnabled"] = False
config["firefoxDarkTheme"] = "firefox-compact-dark@mozilla.org"
config["firefoxLightTheme"] = "firefox-compact-light@mozilla.org"
config["firefoxActiveTheme"] = "firefox-compact-light@mozilla.org"
config["gnomeEnabled"] = False
config["gnomeLightTheme"] = ""
config["gnomeDarkTheme"] = ""
config["kvantumEnabled"] = False
config["kvantumLightTheme"] = ""
config["kvantumDarkTheme"] = ""
config["soundEnabled"] = True

if exists():
    # making config global for this module
    with open(path + "/yin_yang/yin_yang.json", "r") as conf:
        config = json.load(conf)

config["desktop"] = get_desktop()


def get_config():
    """returns the config"""
    return config


def update(key, value):
    """Update the value of a key in configuration"""
    config[key] = value
    write_config()


def write_config(config=config):
    """Write configuration"""
    with open(path + "/yin_yang/yin_yang.json", 'w') as conf:
        json.dump(config, conf, indent=4)


def gtk_exists():
    return os.path.isfile(path + "/gtk-3.0/settings.ini")


def get_enabled_plugins():
    """returns a list of plugins which are activated"""
    pass


def get_light_time():
    """returns the time which should toggle the lightMode"""
    pass


def get_dark_time():
    """returns the time which should toggle the lightMode"""
    pass


def get_theme():
    return config["theme"]


def get_kde_light_theme():
    return config["kdeLightTheme"]


def get_kde_dark_theme():
    return config["kdeDarkTheme"]


def get_kde_enabled():
    return config["kdeEnabled"]


def get_code_light_theme():
    return config["codeLightTheme"]


def get_code_dark_theme():
    return config["codeDarkTheme"]


def get_code_enabled():
    return config["codeEnabled"]


def get_gtk_light_theme():
    return config["gtkLightTheme"]


def get_gtk_dark_theme():
    return config["gtkDarkTheme"]


def get_gtk_enabled():
    return config["gtkEnabled"]


def get(key):
    """Return the given key from the config"""
    return config[key]


def is_scheduled():
    return config["schedule"]


def get_version():
    return config["version"]


def kde_get_light_theme():
    """Return the KDE light theme specified in the yin-yang config"""
    return config["kdeLightTheme"]


def kde_get_dark_theme():
    """Return the KDE dark theme specified in the yin-yang config"""
    return config["kdeDarkTheme"]


def kde_get_checkbox():
    return config["kdeEnabled"]


def gtk_get_light_theme():
    """Return the  GTK Light theme specified in the yin-yang config"""
    return config["gtkLightTheme"]


def gtk_get_dark_theme():
    """Return the  GTK dark theme specified in the yin-yang config"""
    return config["gtkDarkTheme"]


def sound_get_checkbox():
    return config["soundEnabled"]


def gtk_get_checkbox():
    return config["gtkEnabled"]


def code_get_light_theme():
    """Return the code light theme specified in the yin-yang config"""
    return config["codeLightTheme"]


def code_get_dark_theme():
    """Return the  code dark theme specified in the yin-yang config"""
    return config["codeDarkTheme"]


def code_get_checkbox():
    return config["codeEnabled"]


def gnome_get_light_theme():
    """Return the  Gnome Shell Light theme specified in the yin-yang config"""
    return config["gnomeLightTheme"]


def gnome_get_dark_theme():
    """Return the  Gnome Shell dark theme specified in the yin-yang config"""
    return config["gnomeDarkTheme"]


def gnome_get_checkbox():
    return config["gnomeEnabled"]


def kvantum_get_light_theme():
    """Return the Kvantum Light theme specified in the yin-yang config"""
    return config["kvantumLightTheme"]


def kvantum_get_dark_theme():
    """Return the Kvantum dark theme specified in the yin-yang config"""
    return config["kvantumDarkTheme"]


def kvantum_get_checkbox():
    return config["kvantumEnabled"]
