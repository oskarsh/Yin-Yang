from src.meta import Desktop
from src.plugins import system, colors, gtk, icons, kvantum, wallpaper, custom
from src.plugins import firefox, brave, gedit, only_office
from src.plugins import vscode, atom, konsole
from src.plugins import sound, notify

# NOTE initialize your plugin over here:
# The order in the list specifies the order in the config gui
from src.plugins._plugin import Plugin, ExternalPlugin


def get_plugins(desktop: Desktop) -> [Plugin]:
    return [
        system.System(desktop),
        colors.Colors(desktop),
        gtk.Gtk(desktop),
        icons.Icons(desktop),
        kvantum.Kvantum(),
        wallpaper.Wallpaper(desktop),
        firefox.Firefox(),
        brave.Brave(),
        vscode.Vscode(),
        atom.Atom(),
        gedit.Gedit(),
        only_office.OnlyOffice(),
        konsole.Konsole(),
        custom.Custom(),
        sound.Sound(),
        notify.Notification()
    ]


# this lets us skip all external plugins in yin_yang.py while keeping _plugin "private"
ExternalPlugin = ExternalPlugin
