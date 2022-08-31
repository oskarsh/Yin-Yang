from typing import Optional

from PySide6.QtWidgets import QDialogButtonBox, QVBoxLayout, QWidget, QLineEdit
from PySide6.QtDBus import QDBusConnection, QDBusMessage

from src.enums import Desktop
from ._plugin import PluginDesktopDependent, PluginCommandline, Plugin
from .system import test_gnome_availability


class Wallpaper(PluginDesktopDependent):
    # themes are image file paths

    def __init__(self, desktop: Desktop):
        match desktop:
            case Desktop.KDE:
                super().__init__(_Kde())
            case Desktop.GNOME:
                super().__init__(_Gnome())
            case _:
                raise ValueError('Unsupported desktop environment!')

    @property
    def available(self) -> bool:
        return self.strategy is not None

    def get_input(self, widget):
        widgets = []

        for _ in ['Light', 'Dark']:
            grp = QWidget(widget)
            horizontal_layout = QVBoxLayout(grp)

            line = QLineEdit(grp)
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


class _Kde(Plugin):
    name = 'Wallpaper'

    def __init__(self):
        super().__init__()

    def set_theme(self, theme: str) -> Optional[str]:
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
            '    d.writeConfig("Image", "file:{theme}");'
            '}'
        ])
        connection.call(message)
        # can't check if this worked or not
        return theme

    @property
    def available(self) -> bool:
        # the script change_wallpaper comes with this tool, so we can except that it is available
        return True
