import subprocess
from pathlib import Path

from config import ConfigWatcher, config
from enums import ConfigEvent, Modes

TIMER_PATH = str(Path.home()) + '/.local/share/systemd/user/yin_yang.timer'


def run_command(command, **kwargs):
    return subprocess.run(['systemctl', '--user', command, 'yin_yang.timer'], **kwargs)


class SaveWatcher(ConfigWatcher):
    def notify(self, event: ConfigEvent, values):
        if config.mode.value == Modes.MANUAL.value:
            run_command('stop')
            return

        # update timer times
        with open(TIMER_PATH, 'r') as file:
            lines = file.readlines()

        time_light, time_dark = config.times
        lines[4] = f'OnCalendar={time_light.isoformat()}\n'
        lines[5] = f'OnCalendar={time_dark.isoformat()}\n'

        with open(TIMER_PATH, 'w') as file:
            file.writelines(lines)

        subprocess.run(['systemctl', '--user', 'daemon-reload'])
        run_command('start')


watcher = SaveWatcher()
config.add_event_listener(ConfigEvent.SAVE, watcher)
