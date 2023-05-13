import subprocess
import re

from ..meta import Desktop
from ._plugin import Plugin, PluginDesktopDependent, PluginCommandline


class Colors(PluginDesktopDependent):
    def __init__(self, desktop: Desktop):
        if desktop == Desktop.KDE:
            super().__init__(_KDEColors())
        else:
            super().__init__(None)

    @property
    def strategy(self) -> Plugin:
        return self._strategy_instance


class _KDEColors(PluginCommandline):
    name = "Colors"
    translations = {}

    def __init__(self):
        super().__init__(['plasma-apply-colorscheme', '{theme}'])

    @property
    def available_themes(self) -> dict:

        if self.translations:
            return self.translations

        colors = subprocess.check_output(['plasma-apply-colorscheme', '--list-schemes'],
                                         universal_newlines=True)

        colors = colors.splitlines()
        del colors[0]

        for color in colors:
            color = color.replace(' * ', '')
            color = re.sub(r'\((.*?)\)', '', color).strip()
            self.translations[color] = color

        return self.translations
