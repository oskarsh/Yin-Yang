from src.plugins._plugin import PluginCommandline


class Notification(PluginCommandline):
    def __init__(self):
        super().__init__(['notify-send', 'Theme changed', f'Set the theme to %t',
                          '-a', 'Yin & Yang', '-u', 'low', '--icon', 'yin_yang'])
        self.theme_light = 'Day'
        self.theme_dark = 'Night'
