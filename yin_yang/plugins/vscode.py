import os
import json
import logging
from itertools import chain
from os.path import isdir, isfile
from pathlib import Path

from ._plugin import Plugin, flatpak_system, flatpak_user, snap_path

logger = logging.getLogger(__name__)

extension_paths = [
    str(Path.home() / '.vscode/extensions'),
    str(Path.home() / '.vscode-insiders/extensions'),
    str(Path.home() / '.vscode-oss/extensions'),
    '/usr/lib/code/extensions',
    '/usr/lib/code-insiders/extensions',
    '/usr/share/code/resources/app/extensions',
    '/usr/share/code-insiders/resources/app/extensions',
    '/opt/visual-studio-code/resources/app/extensions/',
    '/opt/visual-studio-code-insiders/resources/app/extensions/',
    str(snap_path('code') / 'usr/share/code/resources/app/extensions/'),
    str(snap_path('code-insiders') / 'usr/share/code-insiders/resources/app/extensions/'),
    str(flatpak_user('com.visualstudio.code') / 'data/vscode/extensions/'),
    str(flatpak_user('com.visualstudio.code-oss') / 'data/vscode/extensions/'),
    str(flatpak_user('com.vscodium.codium') / 'data/codium/extensions/'),
    str(flatpak_system('com.visualstudio.code') / 'files/extra/vscode/resources/app/extensions/'),
    str(flatpak_system('com.visualstudio.code-oss') / 'files/main/resources/app/extensions/'),
    str(flatpak_system('com.vscodium.codium') / 'files/share/codium/resources/app/extensions/')
]


def write_new_settings(settings, path):
    # simple adds a new field to the settings
    settings["workbench.colorTheme"] = "Default"
    with open(path, 'w') as conf:
        json.dump(settings, conf, indent=4)


def get_theme_name(path):
    if not isfile(path):
        return []

    # open metadata
    manifest: dict
    with open(path, 'r') as file:
        manifest = json.load(file)

    if 'contributes' not in manifest:
        return []

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
        self.theme_light = 'Default Light Modern'
        self.theme_dark = 'Default Dark Modern'

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
        config_path = str(Path.home() / '.config/{name}/User/settings.json')
        native_settings = (config_path.format(name=name) for name in possible_editors)

        flatpak_settings = [
            str(flatpak_user('com.visualstudio.code') / 'config/Code/User/settings.json'),
            str(flatpak_user('com.visualstudio.code-oss') / 'config/Code - OSS/User/settings.json'),
            str(flatpak_user('com.vscodium.codium') / 'config/VSCodium/User/settings.json')
        ]

        try:
            for editor in filter(
                    os.path.isfile,
                    chain(native_settings, flatpak_settings)):
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

        for path in filter(isdir, extension_paths):
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
        for path in extension_paths:
            if isdir(path):
                return True
        return False
