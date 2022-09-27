from ._plugin import PluginCommandline, get_stuff_in_dir
from pathlib import Path


class Kvantum(PluginCommandline):
    def __init__(self):
        super().__init__(['kvantummanager', '--set', '{theme}'])
        self.theme_light = 'KvFlatLight'
        self.theme_dark = 'KvFlatDark'

    @property
    def available_themes(self) -> dict:
        if not self.available:
            return {}

        paths = ['/usr/share/Kvantum', str(Path.home()) + '/.config/Kvantum']
        themes = list()
        # At present, it seems that the function of finding themes is based
        # on dirs, but .kvconfig. So some theme will not be recognized. This
        # may be fixed next time
        for path in paths:
            themes = themes + get_stuff_in_dir(path, search_type='dir')
        themes_dict: dict = {}
        assert len(themes) > 0, 'No themes were found'

        themes.sort()
        for theme in themes:
            themes_dict[theme] = theme

        assert themes_dict != {}, 'No themes found!'
        return themes_dict
