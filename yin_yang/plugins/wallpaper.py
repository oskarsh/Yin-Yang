import logging
import subprocess
from pathlib import Path

from PySide6.QtWidgets import QDialogButtonBox, QVBoxLayout, QWidget, QLineEdit
from PySide6.QtDBus import QDBusConnection, QDBusMessage

from ..meta import Desktop
from ._plugin import PluginDesktopDependent, PluginCommandline, Plugin
from .system import test_gnome_availability

logger = logging.getLogger(__name__)


class Wallpaper(PluginDesktopDependent):
    # themes are image file paths

    def __init__(self, desktop: Desktop):
        match desktop:
            case Desktop.KDE:
                super().__init__(_Kde())
            case Desktop.GNOME:
                super().__init__(_Gnome())
            case Desktop.XFCE:
                super().__init__(_Xfce())
            case Desktop.CINNAMON:
                super().__init__(_Cinnamon())
            case _:
                super().__init__(None)

    def get_input(self, widget):
        widgets = []

        for is_dark in [False, True]:
            grp = QWidget(widget)
            horizontal_layout = QVBoxLayout(grp)

            line = QLineEdit(grp)
            line.setText(self.theme_dark if is_dark else self.theme_light)
            horizontal_layout.addWidget(line)

            btn = QDialogButtonBox(grp)
            btn.setStandardButtons(QDialogButtonBox.Open)
            horizontal_layout.addWidget(btn)

            widgets.append(grp)

        return widgets


class _Gnome(PluginCommandline):
    name = 'Wallpaper'

    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://{theme}'])

    def available(self) -> bool:
        return test_gnome_availability(self.command)


def check_theme(theme: str) -> bool:
    if not theme:
        return False
    file = Path(theme)
    if "#" in file.name:
        logger.error('Image files that contain a \'#\' will not work.')
        return False
    if not file.exists():
        logger.error(f'Image {theme} does not exist!')
        return False

    return True


class _Kde(Plugin):
    name = 'Wallpaper'

    def __init__(self):
        super().__init__()
        self._theme_light = None
        self._theme_dark = None

    @property
    def theme_light(self) -> str:
        return self._theme_light

    @theme_light.setter
    def theme_light(self, value: str):
        check_theme(value)
        self._theme_light = value

    @property
    def theme_dark(self) -> str:
        return self._theme_dark

    @theme_dark.setter
    def theme_dark(self, value: str):
        check_theme(value)
        self._theme_dark = value

    def set_theme(self, theme: str):
        connection = QDBusConnection.sessionBus()
        message = QDBusMessage.createMethodCall(
            'org.kde.plasmashell',
            '/PlasmaShell',
            'org.kde.PlasmaShell',
            'evaluateScript',
        )
        message.setArguments([
            'string:'
            'var Desktops = desktops();'
            'for (let i = 0; i < Desktops.length; i++) {'
            '    let d = Desktops[i];'
            '    d.wallpaperPlugin = "org.kde.image";'
            '    d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");'
            f'    d.writeConfig("Image", "file:{theme}");'
            '}'
        ])
        connection.call(message)

    @property
    def available(self) -> bool:
        return True


class _Xfce(PluginCommandline):
    def __init__(self):
        # first, get all monitors
        properties = str(subprocess.check_output(['xfconf-query', '-c', 'xfce4-desktop', '-l']))
        monitor = next(p for p in properties.split('\\n') if p.endswith('/workspace0/last-image'))

        super().__init__(['xfconf-query', '-c', 'xfce4-desktop', '-p', monitor, '-s', '{theme}'])


class _Cinnamon(PluginCommandline):
    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.cinnamon.desktop.background', 'picture-uri', 'file://\"{theme}\"'])

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)
