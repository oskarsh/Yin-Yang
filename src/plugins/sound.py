import os
import subprocess
import sys

from src.plugins._plugin import Plugin


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Sound(Plugin):
    def __init__(self):
        super(Sound, self).__init__()
        self.theme_light = './resources/light.wav'
        self.theme_dark = './resources/dark.wav'

    def set_theme(self, theme: str):
        # noinspection SpellCheckingInspection
        subprocess.run(["paplay", resource_path(theme)])

    @property
    def available(self) -> bool:
        try:
            return subprocess.run(['paplay', '--help'], stdout=subprocess.DEVNULL).returncode == 0
        except FileNotFoundError:
            return False
