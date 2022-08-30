from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialogButtonBox, QVBoxLayout

from ._plugin import PluginDesktopDependent, PluginCommandline
from .system import test_gnome_availability


class Wallpaper(PluginDesktopDependent):
    # themes are image file paths

    def __init__(self, desktop: str):
        match desktop:
            case 'kde':
                super().__init__(_Kde())
            case 'gtk':
                super().__init__(_Gnome())
            case _:
                raise ValueError('Unsupported desktop environment!')

    @property
    def available(self) -> bool:
        return self.strategy is not None

    def get_input(self, widget):
        widgets = []

        for _ in ['Light', 'Dark']:
            grp = QtWidgets.QWidget(widget)
            horizontal_layout = QVBoxLayout(grp)

            line = QtWidgets.QLineEdit(grp)
            horizontal_layout.addWidget(line)

            btn = QtWidgets.QDialogButtonBox(grp)
            btn.setStandardButtons(QDialogButtonBox.Open)
            horizontal_layout.addWidget(btn)

            widgets.append(grp)

        return widgets


class _Gnome(PluginCommandline):
    name = 'Wallpaper'

    def __init__(self):
        super().__init__(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://%t"])

    def available(self) -> bool:
        return test_gnome_availability(self.command)


class _Kde(PluginCommandline):
    name = 'Wallpaper'

    def __init__(self):
        super().__init__(["bash", "./src/change_wallpaper.sh", "%t"])

    @property
    def available(self) -> bool:
        # the script change_wallpaper comes with this tool, so we can except that it is available
        return True
