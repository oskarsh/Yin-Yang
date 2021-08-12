from src.plugins import system, gtk, kvantum, wallpaper, firefox, vscode, atom

# NOTE initialize your plugin over here:
# The order in the list specifies the order in the config gui
from src.plugins._plugin import Plugin

plugins: [Plugin] = [
    system.System(),
    gtk.Gtk(),
    kvantum.Kvantum(),
    wallpaper.Wallpaper(),
    firefox.Firefox(),
    vscode.Vscode(),
    atom.Atom()
]

# this lets us skip all external plugins in yin_yang.py while keeping _plugin "private"
ExternalPlugin = _plugin.ExternalPlugin
