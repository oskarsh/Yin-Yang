from operator import sub
import os
from pathlib import Path
import subprocess

from ._plugin import PluginCommandline


class Kvantum(PluginCommandline):
    def __init__(self):
        super().__init__(['kvantummanager', '--set', '{theme}'])
        self.theme_light = 'KvFlatLight'
        self.theme_dark = 'KvFlat'

    def set_theme(self, theme: str):
        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')
        if not (self.available and self.enabled):
            return
        # insert theme in command and run it
        command = self.insert_theme(theme)
        subprocess.check_call(command)
        subprocess.check_call(
            ['dbus-send', '--session', '--type=signal', 
             '/KGlobalSettings', 'org.kde.KGlobalSettings.notifyChange', 
             'int32:2', 'int32:0']
        )

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
