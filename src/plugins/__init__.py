from src.enums import Desktop
from src.plugins import system, gtk, kvantum, wallpaper, firefox, vscode, atom, sound, notify

# NOTE initialize your plugin over here:
# The order in the list specifies the order in the config gui
from src.plugins._plugin import Plugin, ExternalPlugin


def get_plugins(desktop: Desktop) -> [Plugin]:
    return [
        system.System(desktop),
        gtk.Gtk(desktop),
        kvantum.Kvantum(),
        wallpaper.Wallpaper(desktop),
        firefox.Firefox(),
        vscode.Vscode(),
        atom.Atom(),
        sound.Sound(),
        notify.Notification()
    ]


# this lets us skip all external plugins in yin_yang.py while keeping _plugin "private"
ExternalPlugin = ExternalPlugin
