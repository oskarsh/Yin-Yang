from ._plugin import PluginCommandline


class Notification(PluginCommandline):
    def __init__(self):
        super().__init__(['notify-send', 'Theme changed', 'Set the theme to {theme}',
                          '-a', 'Yin & Yang', '-u', 'low', '--icon', 'yin_yang'])
        self.theme_light = 'Day'
        self.theme_dark = 'Night'
