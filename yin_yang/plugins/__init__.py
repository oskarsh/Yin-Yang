from typing import List
from ..meta import Desktop
from . import system, colors, gtk, icons, kvantum, wallpaper, custom
from . import firefox, only_office, okular
from . import vscode, konsole
from . import notify

# NOTE initialize your plugin over here:
# The order in the list specifies the order in the config gui
from yin_yang.plugins._plugin import Plugin, ExternalPlugin


def get_plugins(desktop: Desktop) -> List[Plugin]:
    return [
        system.System(desktop),
        colors.Colors(desktop),
        gtk.Gtk(desktop),
        icons.Icons(desktop),
        kvantum.Kvantum(),
        wallpaper.Wallpaper(desktop),
        firefox.Firefox(),
        vscode.Vscode(),
        only_office.OnlyOffice(),
        okular.Okular(),
        konsole.Konsole(),
        custom.Custom(),
        notify.Notification()
    ]


# this lets us skip all external plugins in theme_switcher.py while keeping _plugin "private"
ExternalPlugin = ExternalPlugin
