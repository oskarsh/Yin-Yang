from configparser import ConfigParser
from os.path import isfile
from pathlib import Path

from ._plugin import Plugin

config_path = f'{Path.home()}/.config/onlyoffice/DesktopEditors.conf'


class OnlyOffice(Plugin):
    def __init__(self):
        super().__init__()
        self.theme_light = 'theme-light'
        self.theme_dark = 'theme-dark'

    def set_theme(self, theme: str):
        config = ConfigParser()
        config.optionxform = str
        config.read(config_path)
        config['General']['UITheme2'] = theme

        with open(config_path, 'w') as file:
            config.write(file)

    @property
    def available(self) -> bool:
        return isfile(config_path)

    @property
    def available_themes(self) -> dict:
        return {
            'theme-system': 'System',
            'theme-light': 'Light',
            'theme-classic-light': 'Classic light',
            'theme-dark': 'Dark',
            'theme-contrast-dark': 'Dark contrast'
        }
