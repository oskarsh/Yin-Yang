import logging
from configparser import ConfigParser
from os import scandir
from os.path import isdir
from pathlib import Path

from src.plugins._plugin import Plugin

logger = logging.getLogger(__name__)


class Konsole(Plugin):
    global_path = '/usr/share/konsole'

    def __init__(self):
        super().__init__()
        self.theme_light = 'BlackOnWhite'
        self.theme_dark = 'Breeze'

    def set_theme(self, theme: str):
        config = ConfigParser()
        # leave casing as is
        config.optionxform = str
        user_path = str(Path.home()) + '/.local/share/konsole'
        with scandir(user_path) as entries:
            files = [f.path for f in entries if f.is_file() and f.name.endswith('.profile')]

        assert len(files) > 0, 'No profiles found!'

        for config_file in files:
            config.read(config_file)

            try:
                config['Appearance']['ColorScheme'] = theme
            except KeyError as e:
                logger.warning(
                    f"""
                    No key {str(e)} found. Trying to add one. 
                    If this doesnt work, try to change the theme manually once.
                    """)

                if str(e) == '\'Appearance\'':
                    config.add_section('Appearance')
                else:
                    raise e

                with open(config_file, 'w+') as file:
                    config.write(file)

                self.set_theme(theme)
                logger.info('Success!')
                return

            with open(config_file, 'w') as file:
                config.write(file)

    @property
    def available_themes(self) -> dict:
        if not self.available:
            return {}

        with scandir(self.global_path) as entries:
            themes_machine = list(
                f.name.replace('.colorscheme', '') for f in entries
                if f.is_file() and f.name.endswith('.colorscheme'))
        themes_machine.sort()

        themes_dict = {}
        config_parser = ConfigParser()

        for theme in themes_machine:
            config_parser.read(f'{self.global_path}/{theme}.colorscheme')
            theme_name = config_parser['General']['Description']
            themes_dict[theme] = theme_name

        assert themes_dict != {}, 'No themes found!'
        return themes_dict

    @property
    def available(self) -> bool:
        return isdir(self.global_path)
