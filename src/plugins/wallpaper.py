from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialogButtonBox, QVBoxLayout

from ._plugin import PluginDesktopDependent, PluginCommandline


class Wallpaper(PluginDesktopDependent):
    # themes are image file paths

    def __init__(self, theme_light: str, theme_dark: str, desktop: str):
        if desktop == 'kde':
            self.strategy_instance = Kde(theme_light, theme_dark)
        elif desktop == 'gtk':
            self.strategy_instance = Gnome(theme_light, theme_dark)
        else:
            raise ValueError('Unsupported desktop environment!')
        super().__init__(theme_light, theme_dark, desktop)

    @property
    def strategy(self):
        return self.strategy_instance

    @property
    def available(self) -> bool:
        return self.strategy is not None

    def get_input(self, widget):
        widgets = []

        for _ in ['Light', 'Dark']:
            grp = QtWidgets.QWidget(widget)
            horizontal_layout = QVBoxLayout(grp)

            btn = QtWidgets.QDialogButtonBox(grp)
            btn.setStandardButtons(QDialogButtonBox.Open)
            horizontal_layout.addWidget(btn)

            widgets.append(grp)

        return widgets


class Gnome(PluginCommandline):
    def __init__(self, theme_light: str, theme_dark: str):
        super().__init__(theme_light, theme_dark,
                         ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://%t"])


class Kde(PluginCommandline):
    def __init__(self, theme_light: str, theme_dark: str):
        super().__init__(theme_light, theme_dark,
                         ["bash", "./src/change_wallpaper.sh", "%t"])

    @property
    def available(self) -> bool:
        # the script change_wallpaper comes with this tool, so we can except that it is available
        return True
