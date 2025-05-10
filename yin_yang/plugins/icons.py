import configparser
from os import path, scandir
from pathlib import Path

from ..meta import Desktop
from ._plugin import PluginCommandline, PluginDesktopDependent
from .system import test_gnome_availability

theme_directories = ['/usr/share/icons', f'{Path.home()}/.icons']


class Icons(PluginDesktopDependent):
    def __init__(self, desktop: Desktop):
        match desktop:
            case Desktop.MATE:
                super().__init__(_Mate())
            case Desktop.CINNAMON:
                super().__init__(_Cinnamon())
            case Desktop.BUDGIE:
                super().__init__(_Budgie())
            case Desktop.KDE:
                super().__init__(_Kde())
            case _:
                super().__init__(None)


class _Mate(PluginCommandline):
    def __init__(self):
        super().__init__(
            ['dconf', 'write', '/org/mate/desktop/interface/icon-theme', '\"{theme}\"']
        )
        self.theme_light = 'Yaru'
        self.theme_dark = 'Yaru-dark'

    @property
    def available(self):
        return self.check_command(['dconf', 'help'])


class _Cinnamon(PluginCommandline):
    def __init__(self):
        super().__init__(
            [
                'gsettings',
                'set',
                'org.cinnamon.desktop.interface',
                'icon-theme',
                '\"{theme}\"',
            ]
        )
        self.theme_light = 'Mint-X'
        self.theme_dark = 'gnome'

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)


class _Budgie(PluginCommandline):
    def __init__(self):
        super().__init__(
            [
                'gsettings',
                'set',
                'org.gnome.desktop.interface',
                'icon-theme',
                '\"{theme}\"',
            ]
        )
        self.theme_light = 'Default'
        self.theme_dark = 'Default'

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)

    @property
    def available_themes(self) -> dict:
        themes = []

        for directory in theme_directories:
            if not path.isdir(directory):
                continue

            with scandir(directory) as entries:
                themes.extend(
                    d.name
                    for d in entries
                    if d.is_dir() and path.isfile(d.path + '/index.theme')
                )

        return {t: t for t in themes}


class _Kde(PluginCommandline):
    def __init__(self):
        super().__init__(["/usr/lib/plasma-changeicons", r"{theme}"])
        self.theme_light = "breeze"
        self.theme_dark = "breeze-dark"

    @property
    def available_themes(self) -> dict:
        themes = []

        for icon_theme in theme_directories:
            if not path.isdir(icon_theme):
                continue

            for icon_theme_folder in scandir(icon_theme):
                if not all(
                    (
                        icon_theme_folder.is_dir(),
                        path.isfile(icon_theme_folder.path + "/index.theme"),
                        path.isfile(icon_theme_folder.path + "/icon-theme.cache"),
                    )
                ):
                    continue

                theme_parser = configparser.ConfigParser(strict=False)
                theme_parser.read(icon_theme_folder.path + "/index.theme")
                theme_name = theme_parser["Icon Theme"]["Name"]

                themes.append((icon_theme_folder.name, theme_name))

        return dict(themes)

    @property
    def available(self) -> dict:
        return path.isfile("/usr/lib/plasma-changeicons")
