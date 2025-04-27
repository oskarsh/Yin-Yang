import json
import logging
from configparser import ConfigParser
from os.path import isdir
from pathlib import Path

from PySide6.QtWidgets import QGroupBox

from ._plugin import ExternalPlugin

logger = logging.getLogger(__name__)


def get_profile_paths() -> Path:
    path = Path.home() / '.mozilla/firefox/'
    config_parser = ConfigParser()
    config_parser.read(path / 'profiles.ini')
    for section in config_parser:
        if not section.startswith('Profile'):
            continue
        yield path / config_parser[section]['Path']


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

        paths = (p / 'extensions.json' for p in get_profile_paths())
        themes: dict[str, str] = {}

        for path in paths:
            try:
                with open(path, 'r') as file:
                    content = json.load(file)
                    for addon in content['addons']:
                        if addon['type'] == 'theme':
                            themes[addon['id']] = addon['defaultLocale']['name']
            except FileNotFoundError:
                logger.warning(f'Firefox profile has no extensions installed: {path}')
                continue

        assert themes != {}, 'No themes found!'
        return themes

    @property
    def available(self) -> bool:
        return isdir(str(Path.home()) + '/.mozilla/firefox/')

    def get_widget(self, area) -> QGroupBox:
        widget = super().get_widget(area)
        widget.setToolTip("You need to install the Yin-Yang extension for Firefox")

        return widget
