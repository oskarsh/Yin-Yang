from ..meta import Desktop
from ._plugin import PluginDesktopDependent, PluginCommandline


class Icons(PluginDesktopDependent):
    def __init__(self, desktop: Desktop):
        match desktop:
            case Desktop.MATE:
                super().__init__(_Mate())
            case Desktop.CINNAMON:
                super().__init__(_Cinnamon())
            case _:
                super().__init__(None)


class _Mate(PluginCommandline):
    def __init__(self):
        super().__init__(['dconf', 'write', '/org/mate/desktop/interface/icon-theme', '\'{theme}\''])
        self.theme_light = 'Yaru'
        self.theme_dark = 'Yaru-dark'

    @property
    def available(self):
        return self.check_command(['dconf', 'help'])


class _Cinnamon(PluginCommandline):
    def __init__(self):
        super().__init__(['gsettings', 'set', 'org.cinnamon.desktop.interface', 'icon-theme', '\"{theme}\"'])
        self.theme_light = 'Mint-X'
        self.theme_dark = 'gnome'
