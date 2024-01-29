from enum import Enum, auto


class Modes(Enum):
    """Different modes for determining the theme that should be used"""

    MANUAL = 'manual'
    SCHEDULED = 'manual time'
    FOLLOW_SUN = 'sunset to sunrise'


class Desktop(Enum):
    KDE = 'kde'
    GNOME = 'gnome'
    XFCE = 'xfce'
    UNKNOWN = 'unknown'
    MATE = 'mate'
    CINNAMON = 'cinnamon'
    BUDGIE = 'budgie'


class PluginKey(Enum):
    ENABLED = 'enabled'
    THEME_LIGHT = 'light_theme'
    THEME_DARK = 'dark_theme'


class ConfigEvent(Enum):
    CHANGE = auto()
    SAVE = auto()


class FileFormat(Enum):
    PLAIN = auto()
    JSON = auto()
    CONFIG = auto()


class UnsupportedDesktopError(NotImplementedError):
    pass
