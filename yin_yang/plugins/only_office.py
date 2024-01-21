from configparser import ConfigParser
from pathlib import Path

from ..meta import FileFormat
from ._plugin import ConfigFilePlugin, flatpak_user


class OnlyOffice(ConfigFilePlugin):
    def __init__(self):
        super().__init__([
            Path.home() / '.config/onlyoffice/DesktopEditors.conf',
            flatpak_user('org.onlyoffice.desktopeditors') / 'config/onlyoffice/DesktopEditors.conf'
        ], file_format=FileFormat.CONFIG)
        self.theme_light = 'theme-light'
        self.theme_dark = 'theme-dark'

    def update_config(self, config: ConfigParser, theme: str):
        config['General']['UITheme'] = theme
        return config

    @property
    def available_themes(self) -> dict:
        return {
            'theme-system': 'System',
            'theme-light': 'Light',
            'theme-classic-light': 'Classic light',
            'theme-dark': 'Dark',
            'theme-contrast-dark': 'Dark contrast'
        }
