import json
import pwd
import os
import pathlib
import re
import subprocess

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config"


def exists():
    # returns True or False wether Config exists or note
    return os.path.isfile(path+"/yin_yang/yin_yang.json")


def getDesktop():

    # just to get all possible implementations of dekstop variables
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


# generate path for yin-yang if there is none this will be skipped
pathlib.Path(path+"/yin_yang").mkdir(parents=True, exist_ok=True)


# if there is no config generate a generic one
config = {}
config["version"] = "2.0"
config["desktop"] = getDesktop()
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


if (exists()):
    # making config global for this module
    with open(path+"/yin_yang/yin_yang.json", "r") as conf:
        config = json.load(conf)

config["desktop"] = getDesktop()


def getConfig():
    # returns the config
    return config


def update(key, value):
    config[key] = value
    writeConfig()


def writeConfig(config=config):
    with open(path+"/yin_yang/yin_yang.json", 'w') as conf:
        json.dump(config, conf, indent=4)


def GTKExists():
    if (os.path.isfile(path+"/gtk-3.0/settings.ini")):
        return True
    else:
        return False


def getEnabledPlugins():
    # returns a list of plugins which are activated
    pass


def getLightTime():
    # returns the time which should toggle the lightMode
    pass


def getDarkTime():
    # returns the time which should toggle the lightMode
    pass


def getTheme():
    return config["theme"]


def getKdeLightTheme():
    return config["kdeLightTheme"]


def getKdeDarkTheme():
    return config["kdeDarkTheme"]


def getKdeEnabled():
    return config["kdeEnabled"]


def getcodeLightTheme():
    return config["codeLightTheme"]


def getcodeDarkTheme():
    return config["codeDarkTheme"]


def getCodeEnabled():
    return config["codeEnabled"]


def getGtkLightTheme():
    return config["gtkLightTheme"]


def getGtkDarkTheme():
    return config["gtkDarkTheme"]


def getGtkEnabled():
    return config["gtkEnabled"]


def get(key):
    # returns the given key from the config
    return config[key]


def isScheduled():
    if (config["schedule"]):
        return True
    else:
        return False


def getVersion():
    return config["version"]


def kdeGetLightTheme():
    # returns the KDE light theme specified in the yin-yang config
    return config["kdeLightTheme"]


def kdeGetDarkTheme():
    # returns the KDE dark theme specified in the yin-yang config
    return config["kdeDarkTheme"]


def kdeGetCheckbox():
    return config["kdeEnabled"]


def gtkGetLightTheme():
    # returns the  GTK Light theme specified in the yin-yang config
    return config["gtkLightTheme"]


def gtkGetDarkTheme():
    # returns the  GTK dark theme specified in the yin-yang config
    return config["gtkDarkTheme"]


def gtkGetCheckbox():
    return config["gtkEnabled"]


def codeGetLightTheme():
    # returns the code light theme specified in the yin-yang config
    return config["codeLightTheme"]


def codeGetDarkTheme():
    # returns the  code dark theme specified in the yin-yang config
    return config["codeDarkTheme"]


def codeGetCheckbox():
    return config["codeEnabled"]
