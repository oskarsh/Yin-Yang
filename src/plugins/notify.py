import subprocess
from src.plugins._plugin import Plugin


class Notification(Plugin):
    def __init__(self):
        super().__init__()
        self.theme_light = 'Day'
        self.theme_light = 'Night'

    def set_theme(self, theme: str):
        # TODO set an icon
        subprocess.run(['notify-send', f'Set the theme to {theme}', '-a', 'Yin & Yang', '-u', 'low'])

    @property
    def available(self) -> bool:
        try:
            return subprocess.run(['notify-send', '--help'], stdout=subprocess.DEVNULL).returncode == 0
        except FileNotFoundError:
            return False
