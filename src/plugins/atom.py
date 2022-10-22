import re
from os.path import isfile
from pathlib import Path

from ._plugin import Plugin, inplace_change


def get_old_theme(settings):
    """
    Returns the theme that is currently used.
    Uses regex to find the currently used theme, I expect that themes follow this pattern:
    XXXX-XXXX-ui     XXXX-XXXX-syntax
    """
    with open(settings, "r") as file:
        string = file.read()
        themes = re.findall(r'themes: \[[\s]*"([A-Za-z0-9\-]*)"[\s]*"([A-Za-z0-9\-]*)"', string)
        if len(themes) >= 1:
            ui_theme, _ = themes[0]
            used_theme = re.findall('([A-z-A-z]*)-', ui_theme)[0]
            return used_theme


class Atom(Plugin):
    # noinspection SpellCheckingInspection
    config_path = str(Path.home()) + "/.atom/config.cson"

    def __init__(self):
        super().__init__()
        self.theme_light = 'one-light'
        self.theme_dark = 'one-dark'

    def set_theme(self, theme: str):
        if not (self.available and self.enabled):
            return

        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        # getting the old theme first
        current_theme: str = get_old_theme(self.config_path)

        if not current_theme:
            raise ValueError("Current theme could not be determined."
                             "If you see this error, try to set a custom theme once and then try again")

        # updating the old theme with theme specified in config
        inplace_change(self.config_path, current_theme, theme)

    @property
    def available(self) -> bool:
        return isfile(self.config_path)
