from PySide6.QtDBus import QDBusMessage

from ..NotificationHandler import create_dbus_message
from ._plugin import DBusPlugin


class Notification(DBusPlugin):
    def __init__(self):
        super().__init__()
        self.theme_light = 'Day'
        self.theme_dark = 'Night'

    def create_message(self, theme: str) -> QDBusMessage:
        return create_dbus_message('Theme changed', f'Set the theme to {theme}')
