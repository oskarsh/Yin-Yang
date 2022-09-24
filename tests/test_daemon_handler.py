import shutil
import subprocess
import unittest
from datetime import time

import daemon_handler
from config import config
from enums import ConfigEvent, Modes


def notify():
    daemon_handler.watcher.notify(ConfigEvent.SAVE, None)


class DaemonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        shutil.copyfile(daemon_handler.TIMER_PATH, daemon_handler.TIMER_PATH + '_backup')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.move(daemon_handler.TIMER_PATH + '_backup', daemon_handler.TIMER_PATH)

    def test_updates_times(self):
        config.reset()
        config.mode = Modes.SCHEDULED
        time_light = time.fromisoformat('06:00')
        time_dark = time.fromisoformat('18:00')
        config.times = time_light, time_dark

        notify()

        with open(daemon_handler.TIMER_PATH) as file:
            lines = file.readlines()
            light = lines[4]
            dark = lines[5]

        self.assertEqual(f'OnCalendar={time_light.isoformat()}\n', light)
        self.assertEqual(f'OnCalendar={time_dark.isoformat()}\n', dark)

    def test_updates_timer(self):
        config.reset()
        config.mode = Modes.MANUAL
        notify()

        output = daemon_handler.run_command('is-active', stdout=subprocess.PIPE).stdout
        self.assertEqual(b'inactive\n', output)

        config.mode = Modes.SCHEDULED
        notify()

        output = daemon_handler.run_command('is-active', stdout=subprocess.PIPE).stdout
        self.assertEqual(b'active\n', output)


if __name__ == '__main__':
    unittest.main()
