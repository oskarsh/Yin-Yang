import subprocess

from ._plugin import Plugin, get_stuff_in_dir


class Kvantum(Plugin):
    theme_bright = 'KvFlatLight'
    theme_dark = 'KvFlat'

    def set_theme(self, theme: str):
        # uses a Kvantum manager cli to switch to a light theme
        # noinspection SpellCheckingInspection
        subprocess.run(["kvantummanager", "--set", theme])

    @property
    def available_themes(self) -> dict[str, str]:
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

    @property
    def available(self) -> bool:
        try:
            return subprocess.run(['kvantummanager', '--help']).returncode == 0
        except FileNotFoundError:
            return False
