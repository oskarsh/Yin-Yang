import subprocess
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

    def available(self) -> bool:
        # Runs the first entry in the command list with --help
        try:
            out = subprocess.run(
                [self.command[0], 'get', self.command[2], self.command[3]],
                stdout=subprocess.DEVNULL
            ).stdout
            if out == f'No such schema \"{self.command[2]}\"':
                # in this case, you might want to run https://gist.github.com/atiensivu/fcc3183e9a6fd74ec1a283e3b9ad05f0
                # or you have to install that extension
                return False
        except FileNotFoundError:
            # if no such command is available, the plugin is not available
            return False


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
