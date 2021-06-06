import traceback

from src.config import config
from src.plugins import system, gtk, kvantum, wallpaper, firefox, vscode, atom

# NOTE initialize your plugin over here:
# The order in the list specifies the order in the config gui
from src.plugins._plugin import Plugin

plugins: [Plugin] = [
    system.System(
        config['systemLightTheme'],
        config['systemDarkTheme'],
        config['desktop']),
    gtk.Gtk(
        config['gtkLightTheme'],
        config['gtkDarkTheme'],
        config['desktop']),
    kvantum.Kvantum(
        config['kvantumLightTheme'],
        config['kvantumDarkTheme']),
    wallpaper.Wallpaper(
        config['wallpaperLightTheme'],
        config['wallpaperDarkTheme'],
        config['desktop']),
    firefox.Firefox(
        config['firefoxLightTheme'],
        config['firefoxDarkTheme']
    ),
    vscode.Vscode(
        config['codeLightTheme'],
        config['codeDarkTheme']
    ),
    atom.Atom(
        config['atomLightTheme'],
        config['atomDarkTheme']
    )
]

for plugin in plugins:
    if not plugin.available:
        plugins.pop(plugins.index(plugin))
        continue
    plugin.enabled = config[f'{str(plugin)}Enabled']


def set_mode(dark_mode: bool):
    for pl in plugins:
        if not pl.enabled:
            continue

        print(f'Changing theme in plugin ' + pl.name)
        try:
            pl.set_mode(dark_mode)
        except Exception as e:
            print('Error while changing the theme in plugin ' + pl.name)
            traceback.print_exception(type(e), e, e.__traceback__)
        print()
