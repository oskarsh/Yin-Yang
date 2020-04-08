import os
import pwd
import configparser
from tempfile import mkstemp
from shutil import move
from typing import Dict
from src import config

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = '/home/' + user + '/.mozilla/firefox/'


def get_profiles() -> Dict[str, str]:
    """
    Reads existing profiles

    :return: List of profile-directories as string
    """

    # the list of profiles
    profiles: Dict[str: str] = {}

    # read ini file wich contains the profiles
    firefox_config = configparser.ConfigParser()
    firefox_config.read(path + 'profiles.ini')

    for section in firefox_config.sections():
        for key in firefox_config[section]:
            if key == 'path':
                profiles[section] = path + firefox_config[section][key]

    return profiles


def get_property(line: str) -> str:
    """
    :return: property of line in user.js
    """
    write: bool = False
    content: str = ''
    i = 0

    for letter in line:
        if letter == '\"':
            i += 1
            write = not write
        elif write and i > 2:
            content = content + letter

    return content


def write_new_settings(theme: str, dark: bool):
    """
    Changes or creates the user.js file for every profile.

    :param theme: Firefox theme id
    :param dev_theme: developer theme [dark|light]
    """

    theme_old: str = config.get("firefoxActiveTheme")
    print('Changing "{theme_old}" to "{theme}"'.format(**locals()))
    
    fh, target_file_path = mkstemp()

    # change the theme for every profile
    for profile, profile_path in get_profiles().items():

        # create user.js if it doesn't exist
        if not os.path.isfile(profile_path + '/user.js'):
            file = open(profile_path + '/user.js', 'w+')
            file.close()

        print('Editing config for {profile}'.format(**locals()))

        # rewrite the user.js
        with open(profile_path + '/user.js', 'r') as user_js, open(target_file_path, 'w') as user_cp_js:

            dev_theme: str = ''
            dark_int: int = int(dark is True)

            if dark:
                dev_theme = 'dark'
            else:
                dev_theme = 'light'

            # dont write the settings for the theme in new file,
            # they will be added later
            for line in user_js:
                if 'devtools.theme' in line:
                    pass
                elif 'ui.systemUsesDarkTheme' in line:
                    pass
                elif 'browser.in-content.dark-mode' in line:
                    pass
                else:
                    user_cp_js.write(line)

            # for devtools-sidebar
            user_cp_js.write('user_pref("devtools.theme", "{dev_theme}");'.format(**locals()) + '\n')
            # for extension and websides, like darkreader or about:config
            user_cp_js.write('user_pref("ui.systemUsesDarkTheme", {dark_int});'.format(**locals()) + '\n')
            # additional stuff like error pages
            user_cp_js.write('user_pref("browser.in-content.dark-mode", {dark});'.format(**locals()) + '\n')

        os.remove(profile_path + '/user.js')
        move(target_file_path, profile_path + '/user.js')

    # The actual ui theme can only be edited via the extension.
    # This is handled with communication.py
    config.update("firefoxActiveTheme", theme)


def switch_to_light():
    # TODO: only standard themes supported right now
    write_new_settings(config.get("firefoxLightTheme"), False)


def switch_to_dark():
    write_new_settings(config.get("firefoxDarkTheme"), True)
