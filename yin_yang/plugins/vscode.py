import json
import logging
import os
from os.path import isdir, isfile
from pathlib import Path

from .. import helpers
from ..meta import FileFormat
from ._plugin import flatpak_system, flatpak_user, snap_path, ConfigFilePlugin

logger = logging.getLogger(__name__)

extension_paths = [
    str(Path.home() / '.vscode/extensions'),
    str(Path.home() / '.vscode-insiders/extensions'),
    str(Path.home() / '.vscode-oss/extensions'),
    helpers.get_usr() + 'lib/code/extensions',
    helpers.get_usr() + 'lib/code-insiders/extensions',
    helpers.get_usr() + 'share/code/resources/app/extensions',
    helpers.get_usr() + 'share/code-insiders/resources/app/extensions',
    '/usr/share/vscodium/resources/app/extensions',
    '/usr/share/vscodium-git/resources/app/extensions',
    '/usr/share/vscodium-insiders/resources/app/extensions',
    '/usr/share/vscodium-insiders-bin/resources/app/extensions',
    '/opt/visual-studio-code/resources/app/extensions/',
    '/opt/visual-studio-code-insiders/resources/app/extensions/',
    '/opt/vscodium-bin/resources/app/extensions/',
    str(snap_path('code') / 'usr/share/code/resources/app/extensions/'),
    str(snap_path('code-insiders') / 'usr/share/code-insiders/resources/app/extensions/'),
    str(flatpak_user('com.visualstudio.code') / 'data/vscode/extensions/'),
    str(flatpak_user('com.visualstudio.code-oss') / 'data/vscode/extensions/'),
    str(flatpak_user('com.vscodium.codium') / 'data/codium/extensions/'),
    str(flatpak_system('com.visualstudio.code') / 'files/extra/vscode/resources/app/extensions/'),
    str(flatpak_system('com.visualstudio.code-oss') / 'files/main/resources/app/extensions/'),
    str(flatpak_system('com.vscodium.codium') / 'files/share/codium/resources/app/extensions/')
]


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


class Vscode(ConfigFilePlugin):
    name = 'VS Code'

    def __init__(self):
        possible_editors = [
            "VSCodium",
            "Code - OSS",
            "Code",
            "Code - Insiders",
        ]
        paths = [Path.home() / f'.config/{name}/User/settings.json' for name in possible_editors]
        paths += [
            flatpak_user('com.visualstudio.code') / 'config/Code/User/settings.json',
            flatpak_user('com.visualstudio.code-oss') / 'config/Code - OSS/User/settings.json',
            flatpak_user('com.vscodium.codium') / 'config/VSCodium/User/settings.json'
        ]
        super(Vscode, self).__init__(paths, file_format=FileFormat.JSON)
        self.theme_light = 'Default Light Modern'
        self.theme_dark = 'Default Dark Modern'

    def update_config(self, config: dict, theme: str):
        config['workbench.colorTheme'] = theme
        return json.dumps(config)

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
    def default_config(self):
        return {'workbench.colorTheme': 'Default'}
