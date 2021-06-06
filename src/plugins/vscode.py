import os
import json
import logging
from os.path import isdir
from pathlib import Path

from ._plugin import Plugin, get_stuff_in_dir


logger = logging.getLogger(__name__)


def write_new_settings(settings, path):
    # simple adds a new field to the settings
    settings["workbench.colorTheme"] = "Default"
    with open(path, 'w') as conf:
        json.dump(settings, conf, indent=4)


class Vscode(Plugin):
    name = 'VS Code'

    def set_theme(self, theme: str):
        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        assert self.available, 'VS Code is not installed!'
        path = str(Path.home()) + "/.config/"

        possible_editors = [
            path + "VSCodium/User/settings.json",
            path + "Code - OSS/User/settings.json",
            path + "Code/User/settings.json",
            path + "Code - Insiders/User/settings.json",
        ]

        for editor in possible_editors:
            if os.path.isfile(editor):
                # getting the old theme to replace it
                with open(editor, "r") as sett:
                    try:
                        settings = json.load(sett)
                    except json.decoder.JSONDecodeError:
                        settings = {"workbench.colorTheme": ""}
                settings['workbench.colorTheme'] = theme
                with open(editor, 'w') as sett:
                    json.dump(settings, sett)

                return theme

            raise FileNotFoundError('No config file found.'
                                    'If you see this error try, to set a custom theme manually once and try again.')

    @property
    def available_themes(self) -> dict:
        paths = ['/usr/lib/code/extensions',
                 str(Path.home()) + '/.vscode-oss/extensions']
        themes_dict = {}
        if not self.available:
            return themes_dict

        for path in paths:
            extension_dirs = get_stuff_in_dir(path, type='dir')
            # filter for a dir that doesnt seem to be an extension
            # since it has no manifest
            if 'node_modules' in extension_dirs:
                extension_dirs.pop(extension_dirs.index('node_modules'))

            for extension_dir in extension_dirs:
                try:
                    with open(f'{path}/{extension_dir}/package.json', 'r') as file:
                        manifest = json.load(file)

                    try:
                        if 'Themes' not in manifest['categories']:
                            continue
                    except KeyError:
                        pass
                    try:
                        if 'themes' not in manifest['contributes']:
                            continue
                    except KeyError:
                        pass

                    try:
                        themes: list = manifest['contributes']['themes']

                        for theme in themes:
                            if 'id' in theme:
                                themes_dict[theme['id']] = theme['id']
                            else:
                                themes_dict[theme['label']] = theme['label']
                    except KeyError as e:
                        logger.error(str(e))
                        continue

                except FileNotFoundError as e:
                    logger.error(str(e))
                    themes_dict = {}
                    break

        assert themes_dict != {}, 'No themes found'
        return themes_dict

    def __str__(self):
        # for backwards compatibility
        return 'code'

    @property
    def available(self) -> bool:
        return isdir('/usr/lib/code/extensions')
