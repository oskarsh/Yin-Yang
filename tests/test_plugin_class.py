import unittest

from src.plugins._plugin import PluginCommandline, Plugin


class MinimalPlugin(Plugin):
    def set_theme(self, theme: str) -> str:
        print(f'Changing to theme {theme}')
        return theme


class GenericTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.plugin = MinimalPlugin(theme_dark='dark', theme_bright='light')

    def test_initialization(self):
        self.assertEqual('dark', self.plugin.theme_dark)
        self.assertEqual('light', self.plugin.theme_bright)
        self.assertEqual('MinimalPlugin', self.plugin.name,
                         'All plugins should use their class name as name by default')
        self.assertEqual('minimalplugin', str(self.plugin),
                         'The string method should return an all lowercase version')

    def test_properties(self):
        self.assertTrue(self.plugin.available,
                        'All plugins should be available by default')
        self.assertDictEqual({}, self.plugin.available_themes,
                             'Available plugins should be empty if not implemented')

    def test_set_theme(self):
        self.assertEqual(False, self.plugin.set_mode(False),
                         'Plugin should return False if it is not enabled')

        self.plugin.enabled = True
        self.assertEqual(True, self.plugin.set_mode(False))
        self.assertEqual(True, self.plugin.set_mode(True))


class CommandlineTest(unittest.TestCase):
    def test_command_substitution(self):
        plugin = PluginCommandline('light', 'dark', ['command', '%t', 'argument'])
        self.assertEqual(['command', 'theme', 'argument'], plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name')

        plugin = PluginCommandline('light', 'dark', ['command', '%targument'])
        self.assertEqual(['command', 'themeargument'],
                         plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name, even if it is inside of an argument')

        plugin = PluginCommandline('light', 'dark', ['command', 'argument%t'])
        self.assertEqual(['command', 'argumenttheme'],
                         plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name, even if it is inside of an argument')

        plugin = PluginCommandline('light', 'dark', ['command', 'argu%tment'])
        self.assertEqual(['command', 'arguthemement'],
                         plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name, even if it is inside of an argument')


if __name__ == '__main__':
    unittest.main()
