from pathlib import Path

from ._plugin import ConfigFilePlugin


class OnlyOffice(ConfigFilePlugin):
    def __init__(self):
        super().__init__([Path.home() / '.config/onlyoffice/DesktopEditors.conf'])
        self.theme_light = 'theme-light'
        self.theme_dark = 'theme-dark'

    def update_config(self, config, theme: str):
        config['General']['UITheme2'] = theme
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
