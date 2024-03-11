import logging
import subprocess
from logging import Handler

logger = logging.getLogger()

class NotificationHandler(Handler):
    """Shows logs as notifications"""
    def emit(self, record):
        try:
            # TODO: This needs to be updated to work with Flatpak
            subprocess.call(['notify-send', record.levelname, record.msg,
                            '-a', 'Yin & Yang', '-u', 'low', '--icon', 'yin_yang'])
        except FileNotFoundError:
            logger.warn('notify-send not found. Notifications will not work!')
