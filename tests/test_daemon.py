import unittest
from datetime import time

from yin_yang.theme_switcher import should_be_dark


class DaemonTest(unittest.TestCase):
    def test_compare_time(self):
        time_light = time.fromisoformat('08:00')
        time_dark = time.fromisoformat('20:00')

        for time_current in [time.fromisoformat('05:00'),
                             time_dark,
                             time.fromisoformat('22:00'),
                             time.fromisoformat('00:00')]:
            with self.subTest('Dark mode should be activated!', time_current=time_current, light_before_dark=True):
                self.assertTrue(should_be_dark(time_current, time_light, time_dark))
            with self.subTest('Light mode should be activated', time_current=time_current, light_before_dark=False):
                self.assertFalse(should_be_dark(time_current, time_dark, time_light))

        for time_current in [time_light,
                             time.fromisoformat('12:00')]:
            with self.subTest('Light mode should be activated!', time_current=time_current, light_before_dark=True):
                self.assertFalse(should_be_dark(time_current, time_light, time_dark))
            with self.subTest('Dark mode should be activated!', time_current=time_current, light_before_dark=False):
                self.assertTrue(should_be_dark(time_current, time_dark, time_light))

        message = 'Light mode should always be enabled if times are equal'
        self.assertFalse(should_be_dark(time.fromisoformat('05:00'), time_dark, time_dark), message)
        self.assertFalse(should_be_dark(time_dark, time_dark, time_dark), message)
        self.assertFalse(should_be_dark(time.fromisoformat('22:00'), time_dark, time_dark), message)


if __name__ == '__main__':
    unittest.main()
