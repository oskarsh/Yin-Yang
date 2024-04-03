import subprocess
from logging import Handler


class NotificationHandler(Handler):
    """Shows logs as notifications"""
    def emit(self, record):
        subprocess.call(['notify-send', record.levelname, str(record.msg),
                         '-a', 'Yin & Yang', '-u', 'low', '--icon', 'yin_yang'])
