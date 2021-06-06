import subprocess
import pwd
import os

from src.plugins._plugin import Plugin, PluginDesktopDependent, PluginCommandline


class System(PluginDesktopDependent):
    def __init__(self, theme_light: str, theme_dark: str, desktop: str):
        if desktop == 'kde':
            self._strategy_instance = Kde(theme_light, theme_dark)
        elif desktop == 'gtk':
            self._strategy_instance = Gnome(theme_light, theme_dark)
        else:
            raise ValueError('Unsupported desktop environment!')
        super().__init__(theme_light, theme_dark, desktop)

    @property
    def strategy(self) -> Plugin:
        return self._strategy_instance


class Gnome(PluginCommandline):
    # TODO allow using the default themes, not only user themes

    def __init__(self, theme_light: str, theme_dark: str):
        super().__init__(theme_light, theme_dark,
                         ["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", "%t"])

    @property
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


def get_readable_kde_theme_name(file) -> str:
    """Searches for the long_name in the file and maps it to the found short name"""

    for line in file:
        if 'Name=' in line:
            name: str = ''
            write: bool = False
            for letter in line:
                if letter == '\n':
                    write = False
                if write:
                    name += letter
                if letter == '=':
                    write = True
            return name


class Kde(Plugin):
    name = 'KDE'
    translations = {}

    @property
    def available_themes(self) -> dict:
        if self.translations != {}:
            return self.translations

        # aliases for path to use later on
        user = pwd.getpwuid(os.getuid())[0]
        path = "/home/" + user + "/.local/share/plasma/look-and-feel/"

        # asks the system what themes are available
        # noinspection SpellCheckingInspection
        long_names = subprocess.check_output(["lookandfeeltool", "-l"], universal_newlines=True)
        long_names = long_names.splitlines()
        long_names.sort()

        # get the actual name
        for long_name in long_names:
            # trying to get the Desktop file
            try:
                # load the name from the metadata.desktop file
                with open(f'/usr/share/plasma/look-and-feel/{long_name}/metadata.desktop', 'r') as file:
                    self.translations[long_name] = get_readable_kde_theme_name(file)
            except OSError:
                # check the next path if the themes exist there
                try:
                    # load the name from the metadata.desktop file
                    with open('{path}{long_name}/metadata.desktop'.format(**locals()), 'r') as file:
                        # search for the name
                        self.translations[long_name] = get_readable_kde_theme_name(file)
                except OSError:
                    # if no file exist lets just use the long name
                    self.translations[long_name] = long_name

        return self.translations

    def set_theme(self, theme: str):
        # uses a kde api to switch to a light theme
        # noinspection SpellCheckingInspection
        subprocess.run(["lookandfeeltool", "-a", theme])
