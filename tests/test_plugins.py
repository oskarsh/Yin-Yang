import unittest

from src.config import config
from src.plugins import plugins
from src.plugins._plugin import Plugin


class PluginsTest(unittest.TestCase):
    def test_setup(self):
        for pl in plugins:
            with self.subTest(plugin=pl.name):
                self.assertIsInstance(pl, Plugin,
                                      'Every plugin should extend the Plugin class')
                self.assertTrue(pl.name != '',
                                'Every plugin needs a name for the config and the gui.')
                if pl.available:
                    self.assertIsInstance(pl.available_themes, dict,
                                          'Available themes always should be a dict.')

    # NOTE if you want to test that your theme changes, set this value to true
    @unittest.skipUnless(False, 'test_theme_changes is disabled')
    def test_set_theme_works(self):
        for pl in plugins:
            with self.subTest(plugin=pl.name):
                if pl.enabled:
                    pl.set_mode(config.dark_mode)


if __name__ == '__main__':
    unittest.main()
