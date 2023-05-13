import json
import struct
import sys
import unittest
from datetime import datetime, time
from subprocess import Popen, PIPE

from yin_yang import communicate
from yin_yang.meta import PluginKey
from yin_yang.config import config
from yin_yang.theme_switcher import should_be_dark


def should_be_dark_extensions(time_current: int, time_dark: int):
    """Determines if dark mode should be active like the extensions do"""
    return time_dark <= time_current


class CommunicationTest(unittest.TestCase):
    def test_move_time(self):
        time_light = time.fromisoformat('07:00')
        time_dark = time.fromisoformat('20:00')

        times = [
            # morning
            datetime.strptime('03:00', '%H:%M'),
            # day
            datetime.strptime('12:00', '%H:%M'),
            # night
            datetime.strptime('22:00', '%H:%M')
        ]

        for time_current in times:
            time_current_str = time_current.strftime('%H:%M')
            with self.subTest('Current time should always be between dark and light',
                              time_current=time_current_str):
                time_current_unix = time_current.timestamp()
                time_light_unix, time_dark_unix = communicate._move_times(time_current, time_light, time_dark)
                self.assertIsInstance(time_light_unix, int)
                self.assertIsInstance(time_dark_unix, int)
                self.assertTrue(time_light_unix <= time_current_unix <= time_dark_unix or
                                time_dark_unix <= time_current_unix <= time_light_unix)

                # test with swapped times
                time_light_unix, time_dark_unix = communicate._move_times(time_current, time_dark, time_light)
                self.assertTrue(time_light_unix <= time_current_unix <= time_dark_unix or
                                time_dark_unix <= time_current_unix <= time_light_unix)

    @unittest.skipUnless(config.get_plugin_key('firefox', PluginKey.ENABLED), 'Firefox plugin is disabled')
    def test_message_build(self):
        message = communicate.send_config('firefox')
        self.assertNotEqual(message, None,
                            'Message should not be empty')
        self.assertNotEqual(message, {},
                            'Message should not be empty')
        self.assertIsInstance(message['enabled'], bool)
        self.assertIsInstance(message['dark_mode'], bool)
        if message['enabled']:
            self.assertIsInstance(message['scheduled'], bool)
            self.assertIsInstance(message['themes'][0], str)
            self.assertIsInstance(message['themes'][1], str)
            if message['scheduled']:
                time_dark, time_light = message['times']
                self.assertIsInstance(time_light, int)
                self.assertIsInstance(time_dark, int)
                time_now = datetime.today().timestamp()
                self.assertTrue(time_light <= time_now < time_dark or time_dark <= time_now < time_light,
                                'Current time should always be between light and dark times')

    @unittest.skipUnless(config.get_plugin_key('firefox', PluginKey.ENABLED), 'Firefox plugin is disabled')
    def test_encode_decode(self):
        process = Popen([sys.executable, '../communicate.py'],
                        stdin=PIPE, stdout=PIPE)
        plugins = ['firefox']

        for plugin in plugins:
            if not config.get_plugin_key(plugin, PluginKey.ENABLED):
                print('Skipped test for ' + plugin)
                continue

            with self.subTest('Returned message should be correct', plugin=plugin):
                # build call
                call_encoded = json.dumps(plugin).encode('utf-8')
                call_encoded = struct.pack(str(len(call_encoded)) + 's',
                                           call_encoded)
                msg_length = struct.pack('=I', len(call_encoded))

                # send call and get response
                process.stdin.write(msg_length)
                process.stdin.write(call_encoded)
                process.stdin.flush()
                process.stdin.close()
                response = process.stdout.readline()
                process.terminate()

                self.assertTrue(response is not None and len(response) > 0,
                                'Response should not be empty')

                # decode response
                response_length = struct.unpack('=I', response[:4])[0]
                response = response[4:]
                response_decoded = response[:response_length].decode('utf-8')
                response_decoded = json.loads(response_decoded)

                # test if correct
                message_expected = communicate.send_config(plugin)
                self.assertDictEqual(message_expected, response_decoded,
                                     'Returned message should be equal to the message')

        process.__exit__(None, None, None)

    def test_dark_mode_detection(self):
        time_light, time_dark = config.times

        # get unix times
        time_current = datetime.today()
        time_light_unix, time_dark_unix = communicate._move_times(time_current, time_light, time_dark)

        is_dark = should_be_dark(time_current.time(), time_light, time_dark)
        # NOTE: this should be equal to how the extension calculates the theme
        detected_dark = should_be_dark_extensions(int(time_current.timestamp()),
                                                  time_dark_unix)

        self.assertEqual(is_dark, detected_dark,
                         f'Dark mode should be {"active" if is_dark else "inactive"} at {time_current.isoformat()}')


if __name__ == '__main__':
    unittest.main()
