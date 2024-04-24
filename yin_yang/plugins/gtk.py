import logging
import subprocess
from os import scandir, path
from pathlib import Path

from PySide6.QtDBus import QDBusMessage

from ._plugin import PluginDesktopDependent, PluginCommandline, DBusPlugin, themes_from_theme_directories
from .system import test_gnome_availability
from ..meta import Desktop

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
            case Desktop.MATE:
                super().__init__(_Mate())
            case Desktop.XFCE:
                super().__init__(_Xfce())
            case Desktop.CINNAMON:
                super().__init__(_Cinnamon())
            case Desktop.BUDGIE:
                super().__init__(_Budgie())
            case _:
                super().__init__(None)

    @property
    def available_themes(self) -> dict:
        themes = themes_from_theme_directories('gtk-3.0')
        return {t: t for t in themes}


class _Gnome(PluginCommandline):
    name = 'GTK'

    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', '{theme}'])
        self.theme_light = 'Default'
        self.theme_dark = 'Default'

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)


class _Budgie(PluginCommandline):
    name = 'GTK'

    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', '{theme}'])
        self.theme_light = 'Default'
        self.theme_dark = 'Default'

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)


class _Kde(DBusPlugin):
    @property
    def name(self):
        return 'GTK'

    def __init__(self):
        super().__init__(['org.kde.GtkConfig', '/GtkConfig', 'org.kde.GtkConfig', 'setGtkTheme'])
        self.theme_light = 'Breeze'
        self.theme_dark = 'Breeze'

    def create_message(self, theme: str):
        self.message = QDBusMessage.createMethodCall(*self.message_data)
        self.message.setArguments([theme])

    def set_theme(self, theme: str):
        """Call DBus interface of kde-gtk-config if installed.
        Otherwise try changing xsettingsd's conf and dconf"""

        if self.connection.interface().isServiceRegistered('org.kde.GtkConfig').value():
            logger.debug("Detected kde-gtk-config, use it")
            super().set_theme(theme)
            return

        # User don't have kde-gtk-config installed, try xsettingsd and dconf
        logger.warning('kde-gtk-config not available, trying xsettingsd and dconf')

        # xsettingsd
        xsettingsd_conf_path = Path.home() / '.config/xsettingsd/xsettingsd.conf'
        if not xsettingsd_conf_path.exists():
            logger.warning('xsettingsd not available')
            return
        with open(xsettingsd_conf_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith('Net/ThemeName'):
                    lines[i] = f'Net/ThemeName "{theme}"\n'
                    break
        with open(xsettingsd_conf_path, 'w') as f:
            f.writelines(lines)
        # send signal to read new config
        subprocess.run(['killall', '-HUP', 'xsettingsd'])

        # change dconf db. since dconf sending data as GVariant, use gsettings instead
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', f'{theme}'])
        color_scheme = 'prefer-dark' if theme == self.theme_dark else 'prefer-light'
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'color-scheme', f'{color_scheme}'])


class _Xfce(PluginCommandline):
    def __init__(self):
        super(_Xfce, self).__init__(['xfconf-query', '-c', 'xsettings', '-p', '/Net/ThemeName', '-s', '{theme}'])
        self.theme_light = 'Adwaita'
        self.theme_dark = 'Adwaita-dark'


class _Mate(PluginCommandline):
    def __init__(self):
        super().__init__(['dconf', 'write', '/org/mate/desktop/interface/gtk-theme', '\'{theme}\''])
        self.theme_light = 'Yaru'
        self.theme_dark = 'Yaru-dark'

    @property
    def available(self) -> bool:
        return self.check_command(['dconf', 'help'])


class _Cinnamon(PluginCommandline):
    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.cinnamon.desktop.interface', 'gtk-theme', '\"{theme}\"'])
        self.theme_light = 'Adwaita'
        self.theme_dark = 'Adwaita-dark'

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)
