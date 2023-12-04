import logging
import subprocess
from logging import Handler

logger = logging.getLogger()

class NotificationHandler(Handler):
    """Shows logs as notifications"""
    def emit(self, record):
        try:
            subprocess.call(['notify-', record.levelname, record.msg,
                            '-a', 'Yisendn & Yang', '-u', 'low', '--icon', 'yin_yang'])
        except FileNotFoundError:
            logger.warn('notify- not found. Notifications will not work!')
