import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialogButtonBox, QVBoxLayout

from ._plugin import PluginDesktopDependent, Plugin


class Wallpaper(PluginDesktopDependent):
    def __init__(self, desktop: str):
        if desktop == 'kde':
            self.strategy_instance = Kde()
        elif desktop == 'gtk':
            self.strategy_instance = Gnome()
        else:
            raise ValueError('Unsupported desktop environment!')
        super().__init__(desktop)

    @property
    def strategy(self):
        return self.strategy_instance

    @property
    def available(self) -> bool:
        return self.strategy is not None

    def get_input(self, widget):
        widgets = []

        for theme in ['Light', 'Dark']:
            grp = QtWidgets.QWidget(widget)
            horizontal_layout = QVBoxLayout(grp)

            btn = QtWidgets.QDialogButtonBox(grp)
            btn.setStandardButtons(QDialogButtonBox.Open)
            horizontal_layout.addWidget(btn)

            widgets.append(grp)

        return widgets


class Gnome(Plugin):
    # themes are actually image file paths
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # noinspection SpellCheckingInspection
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background",
                        "picture-uri", "file://" + theme])


class Kde(Plugin):
    # themes are actually image file paths
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        subprocess.run(["./scripts/change_wallpaper.sh", theme])
