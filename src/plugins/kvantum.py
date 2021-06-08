from ._plugin import PluginCommandline, get_stuff_in_dir


class Kvantum(PluginCommandline):
    def __init__(self):
        super().__init__(["kvantummanager", "--set", '%t'])

    @property
    def available_themes(self) -> dict:
        if not self.available:
            return {}

        path = '/usr/share/Kvantum'

        themes = get_stuff_in_dir(path, type='dir')
        themes_dict: dict = {}
        assert len(themes) > 0, 'No themes were found'

        themes.sort()
        for theme in themes:
            themes_dict[theme] = theme

        assert themes_dict != {}, 'No themes found!'
        return themes_dict
