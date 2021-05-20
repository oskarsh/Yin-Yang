import unittest

from src.plugins._plugin import PluginCommandline, Plugin


class MinimalPlugin(Plugin):
    def set_theme(self, theme: str) -> str:
        print(f'Changing to theme {theme}')
        return theme


class PluginClassTest(unittest.TestCase):
    def test_minimal_plugin(self):
        plugin = MinimalPlugin(theme_dark='dark', theme_bright='light')
        self.assertEqual('dark', plugin.theme_dark)
        self.assertEqual('light', plugin.theme_bright)

        self.assertEqual('MinimalPlugin', plugin.name,
                         'All plugins should use their class name as name by default')
        self.assertTrue(plugin.available,
                        'All plugins should be available by default')
        self.assertDictEqual({}, plugin.available_themes,
                             'Available plugins should be empty if not implemented')

        self.assertEqual(None, plugin.set_mode(False),
                         'Plugin should return None if it is not enabled')
        plugin.enabled = True
        self.assertEqual('light', plugin.set_mode(False))
        self.assertEqual('dark', plugin.set_mode(True))
        self.assertEqual('minimalplugin', str(plugin))

    def test_command_substitution(self):
        plugin = PluginCommandline(['command', '%t', 'argument'])
        self.assertEqual(['command', 'theme', 'argument'], plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name')

        plugin = PluginCommandline(['command', '%targument'])
        self.assertEqual(['command', 'themeargument'],
                         plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name, even if it is inside of an argument')

        plugin = PluginCommandline(['command', 'argument%t'])
        self.assertEqual(['command', 'argumenttheme'],
                         plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name, even if it is inside of an argument')

        plugin = PluginCommandline(['command', 'argu%tment'])
        self.assertEqual(['command', 'arguthemement'],
                         plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name, even if it is inside of an argument')


if __name__ == '__main__':
    unittest.main()
