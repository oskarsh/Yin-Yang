import os
from pathlib import Path

import psutil
from PySide6.QtDBus import QDBusConnection, QDBusMessage

from ..meta import FileFormat
from ._plugin import flatpak_user, ConfigFilePlugin


class Okular(ConfigFilePlugin):
    """Inspired by:
    https://gitlab.com/LADlSLAV/yabotss/-/blob/main/darkman_examples_kde_plasma/dark-mode.d/10_set_theme_okular_dark.sh
    """

    def __init__(self):
        super().__init__([
            Path.home() / '.config/okularpartrc',
            flatpak_user('org.kde.okular') / 'config/okularpartrc'
        ], file_format=FileFormat.CONFIG)
        self._theme_light = ''
        self._theme_dark = 'InvertLightness'

    def set_mode(self, dark: bool):
        if not self.enabled:
            return False

        process_ids = [
            proc.pid for proc in psutil.process_iter(['name', 'username'])
            if proc.name() == 'okular' and proc.username() == os.getlogin()
        ]
        # this is if okular is running in a flatpak
        process_ids.append(2)

        connection = QDBusConnection.sessionBus()
        for pid in process_ids:
            message = QDBusMessage.createMethodCall(
                f'org.kde.okular-{pid}',
                '/okular',
                'org.kde.okular',
                'slotSetChangeColors'
            )
            message.setArguments([dark])
            connection.call(message)

        # now change the config for future starts of the app
        self.set_theme(self.theme_dark if dark else self.theme_light, ignore_theme_check=True)

    def update_config(self, config, theme: str) -> str:
        if theme == self.theme_dark:
            if not config.has_section('Document'):
                config.add_section('Document')
            config['Document']['ChangeColors'] = 'true'
        else:
            config.remove_option('Document', 'ChangeColors')
            if len(config.options('Document')) == 0:
                config.remove_section('Document')
        return config

    @property
    def available_themes(self) -> dict:
        # these are color changing modes in Okulars accessibility settings
        return {
            '': 'Invert colors',
            'InvertLightness': 'Invert lightness',
            'InvertLuma': 'Invert luma (sRGB linear)',
            'InvertLumaSymmetric': 'Invert luma (symmetrical)'
        }

    def get_input(self, widget):
        inputs = super().get_input(widget)
        n_items = len(self.available_themes)

        # modify light item to make it clear that this shows the original without modifications
        for i in range(n_items):
            inputs[0].removeItem(0)
        inputs[0].addItem('Don\'t modify anything')

        return inputs

    @property
    def theme_dark(self):
        return self._theme_dark

    @theme_dark.setter
    def theme_dark(self, value):
        self._theme_dark = value

        for config_path in self.config_paths:
            if not config_path.exists():
                continue

            config = self.open_config(config_path)

            # update rendering mode
            if value == '':
                if config.has_section('Document'):
                    config.remove_option('Document', 'RenderMode')
                    if len(config.options('Document')) == 0:
                        config.remove_section('Document')
            else:
                if not config.has_section('Document'):
                    config.add_section('Document')
                config['Document']['RenderMode'] = value

            self.write_config(config, config_path, space_around_delimiters=False)
