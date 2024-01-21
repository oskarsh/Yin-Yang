import logging
import os
import re
import subprocess
from configparser import ConfigParser
from itertools import chain
from pathlib import Path
from shutil import copyfile

import psutil
from PySide6.QtDBus import QDBusConnection, QDBusMessage

from ._plugin import Plugin

logger = logging.getLogger(__name__)


class Konsole(Plugin):
    """
    Themes are profiles. To use a color scheme,
    create a new profile or edit one to use the desired color scheme.
    This is necessary to allow live theme changes.
    """
    global_path = Path('/usr/share/konsole')
    config_path = Path.home() / '.config/konsolerc'

    @property
    def user_path(self) -> Path:
        return Path.home() / '.local/share/konsole'

    def __init__(self):
        super().__init__()
        self._theme_light = 'BlackOnWhite'
        self._theme_dark = 'Breeze'

    @property
    def theme_light(self):
        return self._theme_light

    @theme_light.setter
    def theme_light(self, value):
        self.update_profile(False, value)
        self._theme_light = value

    @property
    def theme_dark(self):
        return self._theme_dark

    @theme_dark.setter
    def theme_dark(self, value):
        self.update_profile(True, value)
        self._theme_dark = value

    def set_mode(self, dark: bool) -> bool:
        # run checks
        if not super().set_mode(dark):
            return False

        profile = 'Dark' if dark else 'Light'

        # update default profile, if application is started afterward
        self.default_profile = profile + '.profile'

        # Set Konsole profile for all sessions

        # Get the process IDs of all running Konsole instances owned by the current user
        process_ids = [
            proc.pid for proc in psutil.process_iter()
            if proc.name() == 'konsole' and proc.username() == os.getlogin()
        ]

        # loop: console processes
        for proc_id in process_ids:
            logger.debug(f'Changing profile in konsole session {proc_id}')
            set_profile(f'org.kde.konsole-{proc_id}', profile)

        set_profile('org.kde.konsole', profile)  # konsole may don't have session dbus like above
        set_profile('org.kde.yakuake', profile)

        process_ids = [
            proc.pid for proc in psutil.process_iter()
            if proc.name() == 'dolphin' and proc.username() == os.getlogin()
        ]

        # loop: dolphin processes
        for proc_id in process_ids:
            logger.debug(f'Changing profile in dolphin session {proc_id}')
            set_profile(f'org.kde.dolphin-{proc_id}', profile)

        return True

    def set_theme(self, theme: str):
        # everything is done in set_mode (above)
        pass

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

    @property
    def default_profile(self):
        value = None
        # cant use config parser because of weird file structure
        with self.config_path.open('r') as file:
            for line in file:
                # Search for the pattern "DefaultProfile=*"
                match = re.search(r'DefaultProfile=(.*)', line)

                # If a match is found, return the content of the wildcard '*'
                if match:
                    value = match.group(1)
                    if not os.path.isfile(self.user_path / value):
                        value = None

        if value is None:
            # use the first found profile
            for file in self.user_path.iterdir():
                if file.suffix == '.profile':
                    value = file.name
                    break
            if value is not None:
                logger.warning(f'No default profile found, using {value} instead.')

        if value is None:
            # create a custom profile manually
            file_content = """[Appearance]
ColorScheme=Breeze

[General]
Command=/bin/bash
Name=Fish
Parent=FALLBACK/
"""

            with (self.user_path / 'Default.profile').open('w') as file:
                file.writelines(file_content)

            self.default_profile = 'Default.profile'

            return 'Default.profile'

        return value

    @default_profile.setter
    def default_profile(self, value: str):
        assert value.endswith('.profile')

        with self.config_path.open('r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                # Search for the pattern "DefaultProfile=*"
                match = re.search(r'DefaultProfile=(.*)', line)

                # If a match is found, return the content of the wildcard '*'
                if match:
                    logger.debug(f'Changing default profile to {value}')
                    lines[i] = f'DefaultProfile={value}\n'
                    break
                else:
                    logger.debug('No default profile found')
        with self.config_path.open('w') as file:
            file.writelines(lines)

    def update_profile(self, dark: bool, theme: str):
        if not self.available or theme == '':
            # theme is empty string on super init
            return

        # update the color scheme setting in either dark or light profile
        logger.debug('Updating konsole profile')

        file_path = self.user_path / ('Dark.profile' if dark else 'Light.profile')
        if not file_path.exists():
            self.create_profiles()

        profile_config = ConfigParser()
        profile_config.optionxform = str
        profile_config.read(file_path)

        try:
            profile_config['Appearance']['ColorScheme'] = theme
        except KeyError:
            profile_config.add_section('Appearance')
            profile_config['Appearance']['ColorScheme'] = theme

        with open(file_path, 'w') as file:
            profile_config.write(file)

    def create_profiles(self):
        logger.debug('Creating new profiles for live-switching between light and dark themes.')
        # copy default profile to create theme profiles
        light_profile = self.user_path / 'Light.profile'
        dark_profile = self.user_path / 'Dark.profile'
        # TODO there is a parent profile section in the profile file, maybe we can use that (in a later version)?
        copyfile(self.user_path / self.default_profile, light_profile)
        copyfile(self.user_path / self.default_profile, dark_profile)

        # Change name in file
        profile_config = ConfigParser()
        profile_config.optionxform = str

        profile_config.read(light_profile)
        profile_config['General']['Name'] = light_profile.stem

        with open(light_profile, 'w') as file:
            profile_config.write(file)

        profile_config.read(dark_profile)
        profile_config['General']['Name'] = dark_profile.stem

        with open(dark_profile, 'w') as file:
            profile_config.write(file)


def set_profile(service: str, profile: str):
    # connect to the session bus
    connection = QDBusConnection.sessionBus()

    # maybe it's possible with pyside6 dbus packages, but this was simpler and worked
    try:
        sessions = subprocess.check_output(f'qdbus {service} | grep "Sessions/"', shell=True)
    except subprocess.CalledProcessError:
        try:
            sessions = subprocess.check_output(
                f'qdbus org.kde.konsole | grep "Sessions/"', shell=True
            )
            logger.debug(f'Found org.kde.konsole, use that instead')
            service = "org.kde.konsole"
        except subprocess.CalledProcessError:
            # happens when dolphins konsole is not opened
            logger.debug(f'No Konsole sessions available in service {service}, skipping')
            return
    sessions = sessions.decode('utf-8').removesuffix('\n').split('\n')

    # loop: process sessions
    for session in sessions:
        logger.debug(f'Changing profile of session {session} to {profile}')
        # set profile
        message = QDBusMessage.createMethodCall(
            service,
            session,
            'org.kde.konsole.Session',
            'setProfile'
        )
        message.setArguments([profile])
        connection.call(message)
