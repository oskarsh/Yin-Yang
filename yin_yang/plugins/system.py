import json
import logging
import subprocess
import pwd
import os
from configparser import ConfigParser
from pathlib import Path

from PySide6.QtCore import QLocale

from ..meta import Desktop
from ._plugin import PluginDesktopDependent, PluginCommandline

logger = logging.getLogger(__name__)


def test_gnome_availability(command) -> bool:
    return PluginCommandline.check_command(
        [command[0], 'get', command[2], command[3]]
    )


class System(PluginDesktopDependent):
    def __init__(self, desktop: Desktop):
        match desktop:
            case Desktop.KDE:
                super().__init__(_Kde())
            case Desktop.GNOME:
                super().__init__(_Gnome())
            case Desktop.MATE:
                super().__init__(_Mate())
            case Desktop.CINNAMON:
                super().__init__(_Cinnamon())
            case Desktop.BUDGIE:
                super().__init__(_Budgie())
            case _:
                super().__init__(None)


class _Gnome(PluginCommandline):
    name = 'System'

    # TODO allow using the default themes, not only user themes

    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.gnome.shell.extensions.user-theme', 'name', '{theme}'])

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)


class _Budgie(PluginCommandline):
    name = 'System'

    def __init__(self):
        super().__init__(['gsettings', 'set', 'com.solus-project.budgie-panel', 'dark-theme', '{theme}'])
        self.theme_light = 'light'
        self.theme_dark = 'dark'

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)

    # Override because budgie uses a switch for dark/light mode
    def insert_theme(self, theme: str) -> list:
        command = self.command.copy()
        match theme.lower():
            case 'dark':
                theme_bool = 'true'
            case 'light':
                theme_bool = 'false'
            case _:
                raise NotImplementedError

        for i, arg in enumerate(command):
            command[i] = arg.format(theme=theme_bool)

        return command

    @property
    def available_themes(self) -> dict:
        themes: dict[str, str] = {'dark': 'Dark', 'light': 'Light'}

        return themes


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


def get_name_key(meta):
    locale = filter(
        lambda name: name in meta['KPlugin'],
        [f'Name[{QLocale().name()}]',
         f'Name[{QLocale().language()}]',
         'Name']
    )
    return next(locale)


class _Kde(PluginCommandline):
    name = 'System'
    translations = {}

    def __init__(self):
        super().__init__(['lookandfeeltool', '-a', '{theme}'])
        self.theme_light = 'org.kde.breeze.desktop'
        self.theme_dark = 'org.kde.breezedark.desktop'

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
                # json in newer versions
                with open(f'/usr/share/plasma/look-and-feel/{long_name}/metadata.json', 'r') as file:
                    meta = json.load(file)
                    key = get_name_key(meta)
                    self.translations[long_name] = meta['KPlugin'][key]
            except OSError:
                try:
                    # load the name from the metadata.desktop file
                    with open(f'/usr/share/plasma/look-and-feel/{long_name}/metadata.desktop', 'r') as file:
                        self.translations[long_name] = get_readable_kde_theme_name(file)
                except OSError:
                    # check the next path if the themes exist there
                    try:
                        # load the name from the metadata.desktop file
                        with open(f'{path}{long_name}/metadata.desktop', 'r') as file:
                            # search for the name
                            self.translations[long_name] = get_readable_kde_theme_name(file)
                    except OSError:
                        # if no file exist lets just use the long name
                        self.translations[long_name] = long_name

        return self.translations


class _Mate(PluginCommandline):
    theme_directories = [Path('/usr/share/themes'), Path.home() / '.themes']

    def __init__(self):
        super().__init__(['dconf', 'write', '/org/mate/marco/general/theme', '\'{theme}\''])
        self.theme_light = 'Yaru'
        self.theme_dark = 'Yaru-dark'

    @property
    def available_themes(self) -> dict:
        themes = []

        for directory in self.theme_directories:
            if not directory.is_dir():
                continue

            for d in directory.iterdir():
                index = d / 'index.theme'
                if not index.is_file():
                    continue

                config = ConfigParser()
                config.read(index)
                try:
                    theme = config['X-GNOME-Metatheme']['MetacityTheme']
                    themes.append(theme)
                except KeyError:
                    continue

        return {t: t for t in themes}

    @property
    def available(self):
        return self.check_command(['dconf', 'help'])


class _Cinnamon(PluginCommandline):
    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.cinnamon.theme', 'name', '\"{theme}\"'])
        self.theme_light = 'Mint-X-Teal'
        self.theme_dark = 'Mint-Y-Dark-Brown'

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)
