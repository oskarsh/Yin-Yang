import itertools
from os import scandir

from src.plugins._plugin import PluginCommandline
from pathlib import Path


class Kvantum(PluginCommandline):
    def __init__(self):
        super().__init__(['kvantummanager', '--set', '{theme}'])
        self.theme_light = 'KvFlatLight'
        self.theme_dark = 'KvFlat'

    @property
    def available_themes(self) -> dict:
        if not self.available:
            return {}

        paths = ['/usr/share/Kvantum', str(Path.home()) + '/.config/Kvantum']
        # At present, it seems that the function of finding themes is based
        # on dirs, but .kvconfig. So some theme will not be recognized. This
        # may be fixed next time
        themes = []
        for path in paths:
            with scandir(path) as entries:
                themes = list(itertools.chain(themes, (f.name for f in entries if f.is_dir())))

        assert len(themes) > 0, 'No themes were found'

        themes.sort()
        themes_dict = {t: t for t in themes}

        assert themes_dict != {}, 'No themes found!'
        return themes_dict
