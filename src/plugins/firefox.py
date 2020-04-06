import os
import pwd
import json
import configparser
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
                profiles[section]=path + firefox_config[section][key]

    return profiles


def write_new_settings(theme: str, dark: bool):

    # change the theme for every profile

    for profile, profile_path in get_profiles().items():

        # TODO: this overrides existing settings
        with open(profile_path + '/user.js', 'w+') as user_js:

            print(
            'Changing "theme_old" to "{theme}" in {profile}'
            .format(**locals()))

            # change theme:
            user_js.write('user_pref(\"extensions.activeThemeID\", \"' + theme + '\");' + '\n')

            # change darkmode in devtools:
            if dark:
                user_js.write('user_pref(\"devtools.theme\", \"dark\");' + '\n')
            else:
                user_js.write('user_pref(\"devtools.theme\", \"light\");' + '\n')

# TODO: only standard themes supported right now


def switch_to_light():
    write_new_settings("firefox-compact-light@mozilla.org", False)


def switch_to_dark():
    write_new_settings("firefox-compact-dark@mozilla.org", True)
