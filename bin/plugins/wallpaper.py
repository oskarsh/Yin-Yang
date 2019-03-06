import subprocess
from bin import config


def switchToDark():
    wallpaper_dark = config.get("wallpaperDarkTheme")
    if wallpaper_dark == "":
        subprocess.run(["notify-send", "looks like no dark wallpaper is set"])
    else:
        inplace_change("./bin/change_wallpaper.sh", "$wallpaper", wallpaper_dark)
        subprocess.run(["sh", "./bin/change_wallpaper.sh"])
        inplace_change("./bin/change_wallpaper.sh", wallpaper_dark, "$wallpaper")


def switchToLight():
    wallpaper_light = config.get("wallpaperLightTheme")
    if wallpaper_light == "":
        subprocess.run(["notify-send", "looks like no light wallpaper is set"])
    else:
        inplace_change("./bin/change_wallpaper.sh", "$wallpaper", wallpaper_light)
        subprocess.run(["sh", "./bin/change_wallpaper.sh"])
        inplace_change("./bin/change_wallpaper.sh", wallpaper_light, "$wallpaper")


def inplace_change(filename, old_string, new_string):
    #
    # @params: config - config to be written into file
    #          path - the path where the config is will be written into
    #           defaults to the default path

    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print(
            'Changing "{old_string}" to "{new_string}" in {filename}'
            .format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)
