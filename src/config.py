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
    word = str(subprocess.check_output(["w"]))
    regexp = re.compile(r'gnome')
    if regexp.search(word):
        return "gtk"
    regexp = re.compile(r'kde')
    if regexp.search(word):
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


def getEditor():
    # checks which editor is currently in use
    if (os.path.isdir(path+"VSCodium/User/")):
        editor = "VSCodium"
        return editor

    if (os.path.isdir(path+"Code - OSS/User/")):
        editor = "Code - OSS"
        return editor
    # if no editor is used
    return ""


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
