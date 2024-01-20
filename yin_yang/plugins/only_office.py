from os.path import isfile
from pathlib import Path

from ._plugin import ConfigFilePlugin


class OnlyOffice(ConfigFilePlugin):
    def __init__(self):
        super().__init__(Path.home() / '.config/onlyoffice/DesktopEditors.conf')
        self.theme_light = 'theme-light'
        self.theme_dark = 'theme-dark'

    def update_config(self, theme: str):
        config = self.config
        config['General']['UITheme2'] = theme
        return config

    @property
    def available(self) -> bool:
        return isfile(self.config_path)

    @property
    def available_themes(self) -> dict:
        return {
            'theme-system': 'System',
            'theme-light': 'Light',
            'theme-classic-light': 'Classic light',
            'theme-dark': 'Dark',
            'theme-contrast-dark': 'Dark contrast'
        }
