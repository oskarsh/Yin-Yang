from logging import Handler

from PySide6.QtDBus import QDBusConnection, QDBusMessage


def create_dbus_message(title: str, body: str):
    message = QDBusMessage.createMethodCall(
        "org.freedesktop.portal.Desktop",
        "/org/freedesktop/portal/desktop",
        "org.freedesktop.portal.Notification",
        "AddNotification",
    )

    notification = {
        "title": title,
        "body": body,
        "icon": "yin_yang",
        "priority": "low",
    }

    message.setArguments(["YingYang.ThemeChanged", notification])

    return message


class NotificationHandler(Handler):
    """Shows logs as notifications"""

    def emit(self, record):
        connection = QDBusConnection.sessionBus()
        message = create_dbus_message(record.levelname, str(record.msg))
        connection.call(message)
