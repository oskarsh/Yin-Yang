import logging
import re
import shutil
from enum import Enum, auto
from pathlib import Path

from yin_yang import helpers

from .config import ConfigWatcher, config
from .meta import ConfigEvent, Modes

logger = logging.getLogger(__name__)
SYSTEMD_PATH = Path.home() / '.local/share/systemd/user'
TIMER_PATH = SYSTEMD_PATH / 'yin_yang.timer'
SERVICE_PATH = SYSTEMD_PATH / 'yin_yang.service'


def create_files():
    logger.debug('Creating systemd files')
    if not SYSTEMD_PATH.is_dir():
        SYSTEMD_PATH.mkdir(parents=True, exist_ok=True)
    if not TIMER_PATH.is_file():
        shutil.copy('./resources/yin_yang.timer', TIMER_PATH)
    if not SERVICE_PATH.is_file():
        shutil.copy('./resources/yin_yang.service', SERVICE_PATH)
    if helpers.is_flatpak():
        with open(SERVICE_PATH, 'r') as service:
            lines = service.readlines()
        with open(SERVICE_PATH, 'w') as service:
            for line in lines:
                service.write(
                    re.sub(
                        'ExecStart=/usr/bin/yin_yang --systemd',
                        'ExecStart='
                        + str(Path.home())
                        + '/.local/share/flatpak/exports/bin/sh.oskar.yin_yang --systemd',
                        line,
                    )
                )


def run_command(command, **kwargs):
    return helpers.run(['systemctl', '--user', command, 'yin_yang.timer'], **kwargs)


def update_times():
    create_files()

    if config.mode == Modes.MANUAL:
        run_command('stop')
        logger.debug('Stopping systemd timer')
        return

    logger.debug('Updating systemd timer')
    # update timer times
    with TIMER_PATH.open('r') as file:
        lines = file.readlines()

    time_light, time_dark = config.times
    lines[4] = f'OnCalendar={time_light}\n'
    lines[5] = f'OnCalendar={time_dark}\n'
    lines[6] = f'OnStartupSec={config.boot_offset}\n'

    with TIMER_PATH.open('w') as file:
        file.writelines(lines)

    helpers.run(['systemctl', '--user', 'daemon-reload'])
    run_command('start')


class SaveWatcher(ConfigWatcher):
    class _UpdateTimerStatus(Enum):
        NO_UPDATE = auto()
        UPDATE_TIMES = auto()  # times are also updated at start
        START = auto()
        STOP = auto()

    def __init__(self):
        self._next_timer_update: SaveWatcher._UpdateTimerStatus = (
            SaveWatcher._UpdateTimerStatus.NO_UPDATE
        )

    def _set_needed_updates(self, change_values):
        assert change_values['old_value'] != change_values['new_value'], 'No change!'

        match change_values['key']:
            case 'mode':
                # careful with changes from scheduled to follow sun here! xD
                if change_values['old_value'] == Modes.MANUAL.value:
                    self._next_timer_update = SaveWatcher._UpdateTimerStatus.START
                elif change_values['new_value'] == Modes.MANUAL.value:
                    self._next_timer_update = SaveWatcher._UpdateTimerStatus.STOP
                else:
                    self._next_timer_update = (
                        SaveWatcher._UpdateTimerStatus.UPDATE_TIMES
                    )
            case 'times' | 'coordinates' | 'boot_offset':
                self._next_timer_update = SaveWatcher._UpdateTimerStatus.UPDATE_TIMES

    def _update_timer(self):
        match self._next_timer_update:
            case SaveWatcher._UpdateTimerStatus.STOP:
                run_command('stop')
            case (
                SaveWatcher._UpdateTimerStatus.UPDATE_TIMES
                | SaveWatcher._UpdateTimerStatus.START
            ):
                update_times()

        self._next_timer_update = SaveWatcher._UpdateTimerStatus.NO_UPDATE

    def notify(self, event: ConfigEvent, values):
        match event:
            case ConfigEvent.CHANGE:
                self._set_needed_updates(values)
            case ConfigEvent.SAVE:
                self._update_timer()


watcher = SaveWatcher()
