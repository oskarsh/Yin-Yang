import logging
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from src.enums import Desktop
from ._plugin import PluginDesktopDependent, Plugin, PluginCommandline
from .system import test_gnome_availability

logger = logging.getLogger(__name__)


class Gtk(PluginDesktopDependent):
    name = 'GTK'

    def __init__(self, desktop: Desktop):
        match desktop:
            case Desktop.KDE:
                super().__init__(_Kde())
            case Desktop.GNOME:
                super().__init__(_Gnome())
                if not self.strategy.available:
                    print('You need to install an extension for gnome to use it. \n'
                          'You can get it from here: https://extensions.gnome.org/extension/19/user-themes/')
            case _:
                super().__init__(None)


class _Gnome(PluginCommandline):
    name = 'GTK'

    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', '{theme}'])

    def available(self) -> bool:
        return test_gnome_availability(self.command)


class _Kde(Plugin):
    name = 'GTK'

    def __init__(self):
        super().__init__()
        self.theme_light = 'Breeze'
        self.theme_dark = 'Breeze'

    def set_theme(self, theme: str) -> Optional[str]:
        conf = ConfigParser()

        for version in ['gtk-3.0', 'gtk-4.0']:
            config_file = str(Path.home()) + f"/.config/{version}/settings.ini"
            conf.read(config_file)

            conf['Settings']['gtk-theme-name'] = theme

            with open(config_file, "w") as file:
                conf.write(file)

        return theme
