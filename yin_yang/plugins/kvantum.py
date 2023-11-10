import os
from pathlib import Path

from ._plugin import PluginCommandline


class Kvantum(PluginCommandline):
    def __init__(self):
        super().__init__(['kvantummanager', '--set', '{theme}'])
        self.theme_light = 'KvFlatLight'
        self.theme_dark = 'KvFlat'

    @classmethod
    def get_kvantum_theme_from_dir(cls, dir):
        result = set()
        for _, _, filenames in os.walk(dir):
            for filename in filenames:
                if filename.endswith('.kvconfig'):
                    result.add(filename[:-9])
        return list(result)

    @property
    def available_themes(self) -> dict:
        if not self.available:
            return {}

        paths = ['/usr/share/Kvantum', str(Path.home()) + '/.config/Kvantum']
        themes = list()
        for path in paths:
            themes = themes + self.get_kvantum_theme_from_dir(path)
        themes_dict: dict = {}
        assert len(themes) > 0, 'No themes were found'

        themes.sort()
        themes_dict = {t: t for t in themes}

        assert themes_dict != {}, 'No themes found!'
        return themes_dict
