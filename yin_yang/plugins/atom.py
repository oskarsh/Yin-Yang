import re
from pathlib import Path

from ._plugin import ConfigFilePlugin


class Atom(ConfigFilePlugin):
    def __init__(self):
        super().__init__([Path.home() / '.atom/config.cson'])
        self.theme_light = 'one-light'
        self.theme_dark = 'one-dark'

    def update_config(self, config: str, theme: str) -> str:
        current_theme = self.current_theme
        if not current_theme:
            raise ValueError("Current theme could not be determined."
                             "If you see this error, try to set a custom theme once and then try again")

        # updating the old theme with theme specified in config
        return config.replace(current_theme, theme)

    @property
    def current_theme(self):
        """
        Returns the theme that is currently used.
        Uses regex to find the currently used theme, I expect that themes follow this pattern:
        XXXX-XXXX-ui     XXXX-XXXX-syntax
        """

        themes = re.findall(r'themes: \[[\s]*"([A-Za-z0-9\-]*)"[\s]*"([A-Za-z0-9\-]*)"', self.config)
        if len(themes) >= 1:
            ui_theme, _ = themes[0]
            used_theme = re.findall('([A-z-A-z]*)-', ui_theme)[0]
            return used_theme
