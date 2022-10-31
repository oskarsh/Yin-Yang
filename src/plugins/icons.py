from meta import Desktop
from src.plugins._plugin import PluginDesktopDependent, PluginCommandline


class Icons(PluginDesktopDependent):
    def __init__(self, desktop: Desktop):
        match desktop:
            case Desktop.MATE:
                super().__init__(_Mate())
            case _:
                super().__init__(None)


class _Mate(PluginCommandline):
    def __init__(self):
        super().__init__(['dconf', 'write', '/org/mate/desktop/interface/icon-theme', '"\'{theme}\'"'])
        self.theme_light = 'Yaru'
        self.theme_dark = 'Yaru-dark'

    @property
    def available(self):
        return self.check_command(['dconf', 'help'])
