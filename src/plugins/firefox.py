import json
from configparser import ConfigParser
from os.path import isdir
from pathlib import Path

from ._plugin import Plugin


def get_default_profile_path() -> str:
    path = str(Path.home()) + '/.mozilla/firefox/'
    config_parser = ConfigParser()
    config_parser.read(path + '/profiles.ini')
    path += config_parser['Profile0']['Path']

    return path


class Firefox(Plugin):
    """This class has no functionality except providing a section in the config"""
    theme_bright = 'firefox-compact-light@mozilla.org'
    theme_dark = 'firefox-compact-dark@mozilla.org'

    def set_theme(self, theme: str):
        pass

    @property
    def available_themes(self) -> dict:
        if not self.available:
            return {}

        path = get_default_profile_path() + '/extensions.json'
        themes: dict[str, str] = {}

        with open(path, 'r') as file:
            content = json.load(file)
            for addon in content['addons']:
                if addon['type'] == 'theme':
                    themes[addon['id']] = addon['defaultLocale']['name']

        assert themes != {}, 'No themes found!'
        return themes

    @property
    def available(self) -> bool:
        return isdir(get_default_profile_path())
