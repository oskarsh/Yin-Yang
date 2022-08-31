import json
from configparser import ConfigParser
from os.path import isdir
from pathlib import Path

from PySide6.QtWidgets import QGroupBox

from ._plugin import ExternalPlugin


def get_default_profile_path() -> str:
    path = str(Path.home()) + '/.mozilla/firefox/'
    config_parser = ConfigParser()
    config_parser.read(path + '/profiles.ini')
    path += config_parser['Profile0']['Path']

    return path


class Firefox(ExternalPlugin):
    """This class has no functionality except providing a section in the config"""

    def __init__(self):
        super().__init__('https://addons.mozilla.org/de/firefox/addon/yin-yang-linux/')
        self.theme_light = 'firefox-compact-light@mozilla.org'
        self.theme_dark = 'firefox-compact-dark@mozilla.org'

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
        return isdir(str(Path.home()) + '/.mozilla/firefox/')

    def get_widget(self, area) -> QGroupBox:
        widget = super().get_widget(area)
        widget.setToolTip("You need to install the Yin-Yang extension for Firefox")

        return widget
