from src.plugins._plugin import Plugin, PluginDesktopDependent
import subprocess
import pwd
import os


class System(PluginDesktopDependent):
    def __init__(self, desktop: str):
        super().__init__(desktop)
        if desktop == 'kde':
            self._strategy_instance = Kde()
        elif desktop == 'gtk':
            self._strategy_instance = Gnome()
        else:
            raise ValueError('Unsupported desktop environment!')

    @property
    def strategy(self) -> Plugin:
        return self._strategy_instance


# WIP: Potential Check for https://gist.github.com/atiensivu/fcc3183e9a6fd74ec1a283e3b9ad05f0
# to reduce common issues, or write it in the FAQ
class Gnome(Plugin):
    name = 'Gnome'
    # TODO set the default theme for gnome
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # Shell theme
        # noinspection SpellCheckingInspection
        subprocess.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name",
                        '"{}"'.format(theme)])


class Kde(Plugin):
    name = 'KDE'
    # noinspection SpellCheckingInspection
    theme_bright = 'org.kde.breeze.desktop'
    # noinspection SpellCheckingInspection
    theme_dark = 'org.kde.breezedark.desktop'
    translations = {}

    def get_themes_available(self) -> dict[str, str]:
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
                    self.translations[long_name] = self.get_short_name(file)
            except OSError:
                # check the next path if the themes exist there
                try:
                    # load the name from the metadata.desktop file
                    with open('{path}{long_name}/metadata.desktop'.format(**locals()), 'r') as file:
                        # search for the name
                        self.translations[long_name] = self.get_short_name(file)
                except OSError:
                    # if no file exist lets just use the long name
                    self.translations[long_name] = long_name

        return self.translations

    def set_theme(self, theme: str):
        # uses a kde api to switch to a light theme
        # noinspection SpellCheckingInspection
        subprocess.run(["lookandfeeltool", "-a", theme])

    def get_short_name(self, file) -> str:
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
