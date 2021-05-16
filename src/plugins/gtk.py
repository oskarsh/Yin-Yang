import subprocess
from configparser import ConfigParser
from pathlib import Path

from src.plugins._plugin import PluginDesktopDependent, Plugin


class Gtk(PluginDesktopDependent):
    name = 'GTK'

    def __init__(self, desktop: str):
        super().__init__(desktop)
        if desktop == 'kde':
            self.strategy_instance = Kde()
        else:
            self.strategy_instance = Gnome()

    @property
    def available(self) -> bool:
        return self.strategy is not None

    @property
    def strategy(self):
        return self.strategy_instance


class Gnome(Plugin):
    # TODO set default theme names
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # noinspection SpellCheckingInspection
        subprocess.run(
            ["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", theme])  # Applications theme


class Kde(Plugin):
    # Breeze theme uses qt color scheme
    theme_bright = 'Breeze'
    theme_dark = 'Breeze'

    def set_theme(self, theme: str):
        config = ConfigParser()
        config_file = str(Path.home()) + "/.config/gtk-3.0/settings.ini"
        config.read(config_file)

        config['Settings']['gtk-theme-name'] = theme

        with open(config_file, "w") as file:
            config.write(file)
