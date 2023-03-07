import logging
import os
import subprocess
from pathlib import Path

import psutil
from PySide6.QtDBus import QDBusConnection, QDBusMessage

from src.plugins._plugin import Plugin

logger = logging.getLogger(__name__)


class Konsole(Plugin):
    """
    Themes are profiles. To use a color scheme,
    create a new profile or edit one to use the desired color scheme.
    This is necessary to allow live theme changes.
    """
    global_path = Path('/usr/share/konsole')

    @property
    def user_path(self) -> Path:
        return Path.home() / '.local/share/konsole'

    def __init__(self):
        super().__init__()
        self.theme_light = 'BlackOnWhite'
        self.theme_dark = 'Breeze'

    def set_theme(self, theme: str):
        # Set Konsole profile for all sessions

        # Get the process IDs of all running Konsole instances owned by the current user
        process_ids = [
            proc.pid for proc in psutil.process_iter(['name', 'username'])
            if proc.info['name'] == 'konsole' and proc.info['username'] == os.getlogin()
        ]

        # loop: console processes
        for proc_id in process_ids:
            set_profile(f'org.kde.konsole-{proc_id}', theme)

        set_profile('org.kde.yakuake', theme)

    @property
    def available_themes(self) -> dict:
        if not self.available:
            return {}

        profile_paths = [
            p.name.removesuffix('.profile') for p in self.user_path.iterdir()
            if p.is_file() and p.suffix == '.profile'
        ]

        return {profile: profile for profile in profile_paths}

    def get_input(self, widget):
        input_widgets = super().get_input(widget)
        for widget in input_widgets:
            widget.setToolTip(
                'Select a profile. '
                'Create new profiles or edit existing ones within Konsole to change the color scheme.'
            )

        return input_widgets

    @property
    def available(self) -> bool:
        return self.global_path.is_dir()


def set_profile(service: str, profile: str):
    # connect to the session bus
    connection = QDBusConnection.sessionBus()

    # maybe it's possible with pyside6 dbus packages, but this was simpler and worked
    sessions = subprocess.check_output(f'qdbus {service} | grep "Sessions/"', shell=True)
    sessions = sessions.decode('utf-8').removesuffix('\n').split('\n')

    # loop: process sessions
    for session in sessions:
        # set profile
        message = QDBusMessage.createMethodCall(
            service,
            session,
            'org.kde.konsole.Session',
            'setProfile'
        )
        message.setArguments([profile])
        connection.call(message)
