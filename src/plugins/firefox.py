import json
from configparser import ConfigParser
from os.path import isdir
from pathlib import Path

from PyQt5.QtWidgets import QGroupBox, QCheckBox

from ._plugin import Plugin


def get_default_profile_path() -> str:
    path = str(Path.home()) + '/.mozilla/firefox/'
    config_parser = ConfigParser()
    config_parser.read(path + '/profiles.ini')
    path += config_parser['Profile0']['Path']

    return path


class Firefox(Plugin):
    """This class has no functionality except providing a section in the config"""

    def __init__(self, theme_bright: str, theme_dark: str):
        self.enabled_value = False
        super().__init__(theme_bright, theme_dark)

    def set_theme(self, theme: str):
        if not (self.available and self.enabled):
            return

        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        # throws error if in debug mode, else ignored
        assert False, 'Changing the theme is only possible from the Firefox plugin'

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

    def get_widget(self, area) -> QGroupBox:
        widget = super().get_widget(area)
        widget.setToolTip("You need to install the Yin-Yang extension for Firefox")

        return widget

    @property
    def enabled(self) -> bool:
        return self.enabled_value

    @enabled.setter
    def enabled(self, value: bool):
        self.enabled_value = value
        if value:
            print(
                'Please remember to install the Yin-Yang plugin in Firefox.\n' +
                'You can get it here: https://addons.mozilla.org/de/firefox/addon/yin-yang-linux/'
            )
