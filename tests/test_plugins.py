import unittest

from yin_yang.config import config
from yin_yang.config import plugins
from yin_yang.plugins._plugin import Plugin, ExternalPlugin


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

    def test_set_empty_theme(self):
        for pl in plugins:
            with self.subTest(plugin=pl):
                try:
                    pl.set_theme('')
                except ValueError as e:
                    self.assertEqual('Theme \"\" is invalid', str(e),
                                     'set_theme() should throw an exception if the theme is empty')
                    return

                self.assertTrue(False,
                                'set_theme() should throw an exception if the theme is empty!')
                # try to return to previous theme
                pl.set_theme(config.get_plugin_key(pl.name + config.get_plugin_key('theme').title() + 'Theme'))

    def test_set_theme_invalid_state(self):
        for pl in plugins:
            with self.subTest(plugin=pl):
                pl.enabled = False

                self.assertFalse(pl.set_mode(True),
                                 'set_theme() should not be successful if the plugin is disabled')

    # NOTE if you want to test that your theme changes, set this value to true
    @unittest.skipUnless(False, 'test_theme_changes is disabled')
    def test_set_theme_works(self):
        for pl in filter(lambda p: not isinstance(p, ExternalPlugin) and p.enabled, plugins):
            with self.subTest('Changing the theme should be successful', plugin=pl.name):
                self.assertTrue(pl.set_mode(True),
                                'set_mode() should be true, indicating that it was successful')
                self.assertTrue(pl.set_mode(False),
                                'set_mode() should be true, indicating that it was successful')


if __name__ == '__main__':
    unittest.main()
