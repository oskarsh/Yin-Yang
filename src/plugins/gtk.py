from configparser import ConfigParser
from pathlib import Path

from ._plugin import PluginDesktopDependent, Plugin, PluginCommandline


class Gtk(PluginDesktopDependent):
    name = 'GTK'

    def __init__(self, theme_light: str, theme_dark: str, desktop: str):
        if desktop == 'kde':
            self.strategy_instance = Kde(theme_light, theme_dark)
        else:
            self.strategy_instance = Gnome(theme_light, theme_dark)
        super().__init__(theme_light, theme_dark,
                         desktop)

    @property
    def strategy(self):
        return self.strategy_instance


class Gnome(PluginCommandline):
    def __init__(self, theme_light: str, theme_dark: str):
        super().__init__(theme_light, theme_dark,
                         ["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", '%t'])


class Kde(Plugin):
    def set_theme(self, theme: str):
        config = ConfigParser()

        for version in ['gtk-3.0', 'gtk-4.0']:
            config_file = str(Path.home()) + f"/.config/{version}/settings.ini"
            config.read(config_file)

            config['Settings']['gtk-theme-name'] = theme

            with open(config_file, "w") as file:
                config.write(file)

        return theme
