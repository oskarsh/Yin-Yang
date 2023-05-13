import unittest

from PySide6.QtGui import QColor

from yin_yang.plugins._plugin import PluginCommandline, Plugin, get_qcolor_from_int, get_int_from_qcolor


class MinimalPlugin(Plugin):
    def __init__(self, theme_dark, theme_light):
        super().__init__()
        self._theme_dark_value = theme_dark
        self._theme_light_value = theme_light
        self._enabled_value = True

    def set_theme(self, theme: str):
        print(f'Changing to theme {theme}')
        if not (self.enabled and self.available):
            return

    @property
    def theme_dark(self) -> str:
        return self._theme_dark_value

    @theme_dark.setter
    def theme_dark(self, value: str):
        self._theme_dark_value = value

    @property
    def theme_light(self) -> str:
        return self._theme_light_value

    @theme_light.setter
    def theme_light(self, value: str):
        self._theme_light_value = value

    @property
    def enabled(self) -> bool:
        return self._enabled_value

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled_value = value


class PluginCommandlineTest(PluginCommandline):
    def __init__(self, command: list, theme_dark: str = None, theme_light: str = None):
        super().__init__(command)
        self._theme_light_value = theme_light
        self._theme_dark_value = theme_dark

    @property
    def theme_light(self) -> str:
        return self._theme_light_value

    @theme_light.setter
    def theme_light(self, value: str):
        self._theme_light_value = value

    @property
    def theme_dark(self) -> str:
        return self._theme_dark_value

    @theme_dark.setter
    def theme_dark(self, value: str):
        self._theme_dark_value = value


class GenericTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.plugin = MinimalPlugin(theme_dark='dark', theme_light='light')

    def test_initialization(self):
        self.assertEqual('dark', self.plugin.theme_dark)
        self.assertEqual('light', self.plugin.theme_light)
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
        self.plugin.enabled = False
        self.assertEqual(False, self.plugin.set_mode(False),
                         'Plugin should return False if it is not enabled')

        self.plugin.enabled = True
        self.assertEqual(True, self.plugin.set_mode(False))
        self.assertEqual(True, self.plugin.set_mode(True))


class CommandlineTest(unittest.TestCase):
    def test_command_substitution(self):
        plugin = PluginCommandlineTest(['command', '{theme}', 'argument'], 'light', 'dark')
        self.assertEqual(['command', 'theme', 'argument'], plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name')

        plugin = PluginCommandlineTest(['command', '{theme}argument'], 'light', 'dark')
        self.assertEqual(['command', 'themeargument'],
                         plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name, even if it is inside of an argument')

        plugin = PluginCommandlineTest(['command', 'argument{theme}'], 'light', 'dark')
        self.assertEqual(['command', 'argumenttheme'],
                         plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name, even if it is inside of an argument')

        plugin = PluginCommandlineTest(['command', 'argu{theme}ment'], 'light', 'dark')
        self.assertEqual(['command', 'arguthemement'],
                         plugin.insert_theme('theme'),
                         'insert_theme should replace %t with the theme name, even if it is inside of an argument')


class UtilityTest(unittest.TestCase):
    def test_color_conversion(self):
        # white
        color_int = -1
        color = get_qcolor_from_int(color_int)
        self.assertEqual(QColor.fromRgb(255, 255, 255), color)
        self.assertEqual(get_int_from_qcolor(color), color_int)

        # black
        color_int = -16777216
        color = get_qcolor_from_int(color_int)
        self.assertEqual(QColor.fromRgb(0, 0, 0), color)
        self.assertEqual(get_int_from_qcolor(color), color_int)


if __name__ == '__main__':
    unittest.main()
