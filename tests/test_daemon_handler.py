import pathlib
import shutil
import subprocess
import unittest
from datetime import time
from os.path import isfile

from yin_yang import daemon_handler
from yin_yang.config import config
from yin_yang.meta import Modes, ConfigEvent


class DaemonTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        config.reset()
        config.add_event_listener(ConfigEvent.CHANGE, daemon_handler.watcher)
        config.add_event_listener(ConfigEvent.SAVE, daemon_handler.watcher)

    def tearDown(self) -> None:
        super().tearDown()
        config.remove_event_listener(ConfigEvent.CHANGE, daemon_handler.watcher)
        config.remove_event_listener(ConfigEvent.SAVE, daemon_handler.watcher)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if not isfile(daemon_handler.TIMER_PATH):
            pathlib.Path(daemon_handler.SYSTEMD_PATH).mkdir(parents=True, exist_ok=True)
            shutil.copyfile('./resources/yin_yang.timer', daemon_handler.TIMER_PATH)
            shutil.copyfile('./resources/yin_yang.service', daemon_handler.SERVICE_PATH)
        shutil.copyfile(daemon_handler.TIMER_PATH, daemon_handler.TIMER_PATH.with_suffix('.timer_backup'))

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.move(daemon_handler.TIMER_PATH.with_suffix('.timer_backup'), daemon_handler.TIMER_PATH)

    def test_starts_stops(self):
        config.mode = Modes.SCHEDULED
        config.save()
        output = daemon_handler.run_command('is-active', stdout=subprocess.PIPE).stdout
        self.assertEqual(b'active\n', output)

        config.mode = Modes.MANUAL
        config.save()
        output = daemon_handler.run_command('is-active', stdout=subprocess.PIPE).stdout
        self.assertEqual(b'inactive\n', output)

        config.mode = Modes.FOLLOW_SUN
        config.save()
        output = daemon_handler.run_command('is-active', stdout=subprocess.PIPE).stdout
        self.assertEqual(b'active\n', output)

    def test_updates_times(self):
        config.mode = Modes.SCHEDULED
        time_light = time(6, 0)
        time_dark = time(18, 0)
        config.times = time_light, time_dark
        config.save()

        light, dark = self.read_times()
        self.assertEqual(f'OnCalendar={time_light.isoformat()}\n', light)
        self.assertEqual(f'OnCalendar={time_dark.isoformat()}\n', dark)

        config.mode = Modes.FOLLOW_SUN
        time_light, time_dark = config.times
        config.save()

        light, dark = self.read_times()
        self.assertEqual(f'OnCalendar={time_light.isoformat()}\n', light)
        self.assertEqual(f'OnCalendar={time_dark.isoformat()}\n', dark)

    @staticmethod
    def read_times():
        with open(daemon_handler.TIMER_PATH, 'r') as file:
            lines = file.readlines()
            light, dark = lines[4:6]
        return light, dark

    def test_updates_timer(self):
        config.mode = Modes.SCHEDULED
        config.save()

        output = daemon_handler.run_command('is-active', stdout=subprocess.PIPE).stdout
        self.assertEqual(b'active\n', output)

        config.mode = Modes.MANUAL
        config.save()

        output = daemon_handler.run_command('is-active', stdout=subprocess.PIPE).stdout
        self.assertEqual(b'inactive\n', output)

        config.mode = Modes.FOLLOW_SUN
        config.save()

        output = daemon_handler.run_command('is-active', stdout=subprocess.PIPE).stdout
        self.assertEqual(b'active\n', output)


if __name__ == '__main__':
    unittest.main()
