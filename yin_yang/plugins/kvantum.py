from os import walk
from pathlib import Path

from yin_yang import helpers

from ._plugin import PluginCommandline


class Kvantum(PluginCommandline):
    def __init__(self):
        super().__init__(['kvantummanager', '--set', '{theme}'])
        self.theme_light = 'KvFlatLight'
        self.theme_dark = 'KvFlat'

    @classmethod
    def get_kvantum_theme_from_dir(cls, directory: Path):
        result = set()
        for _, _, filenames in walk(directory):
            for filename in filenames:
                if filename.endswith('.kvconfig'):
                    result.add(filename[:-9])
        return list(result)

    @property
    def available_themes(self) -> dict:
        if not self.available:
            return {}

        paths = [Path('/usr/share/Kvantum'), Path.home() / '.config/Kvantum']
        # Flatpak doesn't allow direct access to /usr
        if (helpers.is_flatpak()):
            paths[0] = Path('/var/run/host/usr/share/Kvantum')
        themes = list()
        for path in paths:
            themes = themes + self.get_kvantum_theme_from_dir(path)
        assert len(themes) > 0, 'No themes were found'

        themes.sort()
        themes_dict = {t: t for t in themes}

        assert themes_dict != {}, 'No themes found!'
        return themes_dict
