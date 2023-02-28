import logging
from configparser import ConfigParser
from pathlib import Path
from itertools import chain

from src.plugins._plugin import Plugin

logger = logging.getLogger(__name__)


class Konsole(Plugin):
    global_path = Path('/usr/share/konsole')

    @property
    def user_path(self) -> Path:
        return Path.home() / '.local/share/konsole'

    def __init__(self):
        super().__init__()
        self.theme_light = 'BlackOnWhite'
        self.theme_dark = 'Breeze'

    def set_theme(self, theme: str):
        config = ConfigParser()
        # leave casing as is
        config.optionxform = str
        config_paths = [
            p for p in self.user_path.iterdir()
            if p.is_file() and p.suffix == '.profile'
        ]

        assert len(config_paths) > 0, 'No profiles found!'

        for config_path in config_paths:
            config.read(config_path)

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

                with config_path.open('w+') as file:
                    config.write(file)

                self.set_theme(theme)
                logger.info('Success!')
                return

            with config_path.open('w') as file:
                config.write(file)

    @property
    def available_themes(self) -> dict:
        if not self.available:
            return {}

        themes = dict(sorted([
            (p.with_suffix('').name, p)
            for p in chain(self.global_path.iterdir(), self.user_path.iterdir())
            if p.is_file() and p.suffix == '.colorscheme'
        ]))

        themes_dict = {}
        config_parser = ConfigParser()

        for theme, theme_path in themes.items():
            config_parser.read(theme_path)
            theme_name = config_parser['General']['Description']
            themes_dict[theme] = theme_name

        assert themes_dict != {}, 'No themes found!'
        return themes_dict

    @property
    def available(self) -> bool:
        return self.global_path.is_dir()
