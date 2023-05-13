import subprocess

from ._plugin import PluginCommandline


class Sound(PluginCommandline):
    def __init__(self):
        super(Sound, self).__init__(["paplay", '{theme}'])
        self.theme_light = './resources/light.wav'
        self.theme_dark = './resources/dark.wav'

    @property
    def available(self) -> bool:
        try:
            return subprocess.run(['paplay', '--help'], stdout=subprocess.DEVNULL).returncode == 0
        except FileNotFoundError:
            return False
