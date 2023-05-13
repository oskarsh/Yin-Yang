import os
from os.path import isdir
from xml.etree import ElementTree

from ._plugin import PluginCommandline
from .system import test_gnome_availability

path = '/usr/share/gtksourceview-4/styles/'


class Gedit(PluginCommandline):
    def __init__(self):
        super(Gedit, self).__init__(['gsettings', 'set', 'org.gnome.gedit.preferences.editor', 'scheme', '{theme}'])

    @property
    def available(self) -> bool:
        return test_gnome_availability(self.command)

    @property
    def available_themes(self) -> dict:
        if not isdir(path):
            return {}

        themes = {}
        with os.scandir(path) as entries:
            for file in (f.path for f in entries if f.is_file() and not f.name.endswith('.rng')):
                config = ElementTree.parse(file)
                attributes = config.getroot().attrib

                name = attributes.get('_name')
                theme_id = attributes.get('id')
                themes[theme_id] = name if name is not None else theme_id

        return themes
