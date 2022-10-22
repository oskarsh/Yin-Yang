from src.plugins._plugin import PluginCommandline
from src.plugins.system import test_gnome_availability


class Gedit(PluginCommandline):
    def __init__(self):
        super(Gedit, self).__init__(['gsettings', 'set', 'org.gnome.gedit.preferences.editor', 'scheme', '{theme}'])

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)
