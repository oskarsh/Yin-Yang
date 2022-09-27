import logging
import subprocess
from enum import Enum, auto
from pathlib import Path

from src.config import ConfigWatcher
from src.enums import ConfigEvent, Modes

logger = logging.getLogger(__name__)
TIMER_PATH = str(Path.home()) + '/.local/share/systemd/user/yin_yang.timer'


def run_command(command, **kwargs):
    return subprocess.run(['systemctl', '--user', command, 'yin_yang.timer'], **kwargs)


def update_times(saved_config):
    if saved_config['mode'] == Modes.MANUAL.value:
        run_command('stop')
        logger.debug('Stopping systemd timer')
        return

    logger.debug('Updating systemd timer')
    # update timer times
    with open(TIMER_PATH, 'r') as file:
        lines = file.readlines()

    time_light, time_dark = saved_config['times']
    lines[4] = f'OnCalendar={time_light}\n'
    lines[5] = f'OnCalendar={time_dark}\n'

    with open(TIMER_PATH, 'w') as file:
        file.writelines(lines)

    subprocess.run(['systemctl', '--user', 'daemon-reload'])
    run_command('start')


class SaveWatcher(ConfigWatcher):
    class _UpdateTimerStatus(Enum):
        NO_UPDATE = auto()
        UPDATE_TIMES = auto()  # times are also updated at start
        START = auto()
        STOP = auto()

    def __init__(self):
        self._next_timer_update: SaveWatcher._UpdateTimerStatus = SaveWatcher._UpdateTimerStatus.NO_UPDATE

    def _set_needed_updates(self, change_values):
        assert change_values['old_value'] != change_values['new_value'], 'No change!'

        match change_values['key']:
            case 'mode':
                # careful with changes from scheduled to follow sun here! xD
                if change_values['old_value'] == Modes.MANUAL.value:
                    self._next_timer_update = SaveWatcher._UpdateTimerStatus.START
                elif change_values['new_value'] == Modes.MANUAL.value:
                    self._next_timer_update = SaveWatcher._UpdateTimerStatus.STOP
            case 'times' | 'coordinates':
                self._next_timer_update = SaveWatcher._UpdateTimerStatus.UPDATE_TIMES

    def _update_timer(self, values):
        match self._next_timer_update:
            case SaveWatcher._UpdateTimerStatus.STOP:
                run_command('stop')
            case SaveWatcher._UpdateTimerStatus.UPDATE_TIMES | SaveWatcher._UpdateTimerStatus.START:
                update_times(values)

        self._next_timer_update = SaveWatcher._UpdateTimerStatus.NO_UPDATE

    def notify(self, event: ConfigEvent, values):
        match event.value:
            case ConfigEvent.CHANGE.value:
                self._set_needed_updates(values)
            case ConfigEvent.SAVE.value:
                self._update_timer(values)


watcher = SaveWatcher()
