import os
import json
import logging
from os.path import isdir
from pathlib import Path

from ._plugin import Plugin

logger = logging.getLogger(__name__)

EXTENSION_PATHS = [
    str(Path.home()) + '/.vscode/extensions',
    str(Path.home()) + '/.vscode-oss/extensions',
    '/usr/lib/code/extensions',
    '/opt/visual-studio-code/resources/app/extensions/',
    '/var/lib/snapd/snap/code/current/usr/share/code/resources/app/extensions/'
]


def write_new_settings(settings, path):
    # simple adds a new field to the settings
    settings["workbench.colorTheme"] = "Default"
    with open(path, 'w') as conf:
        json.dump(settings, conf, indent=4)


def get_theme_name(path):
    # open metadata
    manifest: dict
    with open(path, 'r') as file:
        manifest = json.load(file)

    # collect themes
    themes: list
    if 'themes' in manifest['contributes']:
        themes = manifest['contributes']['themes']
    elif 'Themes' in manifest['contributes']:
        themes = manifest['contributes']['Themes']
    else:
        return []

    return (theme['id'] if 'id' in theme else theme['label'] for theme in themes)


class Vscode(Plugin):
    name = 'VS Code'

    def __init__(self):
        super(Vscode, self).__init__()
        self.theme_light = 'Default Light+'
        self.theme_dark = 'Default Dark+'

    def set_theme(self, theme: str):
        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        if not (self.available and self.enabled):
            return

        possible_editors = [
            "VSCodium",
            "Code - OSS",
            "Code",
            "Code - Insiders",
        ]

        try:
            for editor in filter(
                    os.path.isfile,
                    (f'{str(Path.home())}/.config/{name}/User/settings.json' for name in possible_editors)):
                # load the settings
                with open(editor, "r") as sett:
                    try:
                        settings = json.load(sett)
                        settings['workbench.colorTheme'] = theme
                    except json.decoder.JSONDecodeError as e:
                        # check if the file is completely empty
                        sett.seek(0)
                        first_char: str = sett.read(1)
                        if not first_char:
                            # file is empty
                            logger.info('File is empty')
                            settings = {"workbench.colorTheme": theme}
                        else:
                            # settings file is malformed
                            raise e

                # write changed settings into the file
                with open(editor, 'w') as sett:
                    json.dump(settings, sett)
        except StopIteration:
            raise FileNotFoundError('No config file found. '
                                    'If you see this error, try to set a custom theme manually once and try again.')

    @property
    def available_themes(self) -> dict:
        themes_dict = {}
        if not self.available:
            return themes_dict

        for path in filter(isdir, EXTENSION_PATHS):
            with os.scandir(path) as entries:
                for d in entries:
                    # filter for a dir that doesn't seem to be an extension
                    # since it has no manifest
                    if not d.is_dir() or d.name == 'node_modules':
                        continue

                    for theme_name in get_theme_name(f'{d.path}/package.json'):
                        themes_dict[theme_name] = theme_name

        assert themes_dict != {}, 'No themes found'
        return themes_dict

    def __str__(self):
        # for backwards compatibility
        return 'code'

    @property
    def available(self) -> bool:
        for path in EXTENSION_PATHS:
            if isdir(path):
                return True
        return False
