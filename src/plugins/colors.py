import pwd
import subprocess
import re

from src import config
from src.plugins._plugin import Plugin, PluginDesktopDependent, PluginCommandline

class Colors(PluginDesktopDependent):
    def __init__(self):
        desktop = config.get('desktop')
        if desktop == 'kde':
            self._strategy_instance = _KDEColors()
        else:
            raise ValueError('Unsupported desktop environment!')
        super().__init__()

    @property
    def strategy(self) -> Plugin:
        return self._strategy_instance


class _KDEColors(PluginCommandline):
    name = "Colors"
    translations = {}

    def __init__(self):
        super().__init__(['plasma-apply-colorscheme', '%t'])

    @property
    def available_themes(self) -> dict:

        if self.translations:
            return self.translations

        colors = subprocess.check_output(['plasma-apply-colorscheme', '--list-schemes'], 
            universal_newlines=True)

        colors = colors.splitlines()
        del colors[0]
        colors.sort()

        for color in colors:
            color = color.replace('*', '').replace(' ', '')
            color = re.sub(r'\((.*?)\)', '', color)
            self.translations[color] = color

        return self.translations