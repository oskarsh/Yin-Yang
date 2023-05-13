import unittest
from datetime import time
from pathlib import Path
from typing import Optional

from yin_yang.config import config, ConfigWatcher, update_config
from yin_yang.meta import Desktop, Modes, PluginKey, ConfigEvent

config_path = f"{Path.home()}/.config/yin_yang/yin_yang_dev.json"

old_configs = {
    2.1: {
        "version": 2.1,
        "desktop": "kde",
        "followSun": False,
        "latitude": "",
        "longitude": "",
        "schedule": True,
        "switchToDark": "20:0",
        "switchToLight": "7:0",
        "running": False,
        "theme": "",
        "codeLightTheme": "Default Light+",
        "codeDarkTheme": "Default Dark+",
        "codeEnabled": False,
        "kdeLightTheme": "org.kde.breeze.desktop",
        "kdeDarkTheme": "org.kde.breezedark.desktop",
        "kdeEnabled": False,
        "gtkLightTheme": "",
        "gtkDarkTheme": "",
        "atomLightTheme": "",
        "atomDarkTheme": "",
        "atomEnabled": False,
        "gtkEnabled": False,
        "wallpaperLightTheme": "",
        "wallpaperDarkTheme": "",
        "wallpaperEnabled": False,
        "firefoxEnabled": False,
        "firefoxDarkTheme": "firefox-compact-dark@mozilla.org",
        "firefoxLightTheme": "firefox-compact-light@mozilla.org",
        "firefoxActiveTheme": "firefox-compact-light@mozilla.org",
        "gnomeEnabled": False,
        "gnomeLightTheme": "",
        "gnomeDarkTheme": "",
        "kvantumEnabled": False,
        "kvantumLightTheme": "",
        "kvantumDarkTheme": "",
        "soundEnabled": False
    },
    2.2: {
        "version": 2.2,
        "desktop": "kde",
        "followSun": False,
        "latitude": "",
        "longitude": "",
        "schedule": True,
        "switchToDark": "20:0",
        "switchToLight": "7:0",
        "running": False,
        "theme": "",
        "codeLightTheme": "Default Light+",
        "codeDarkTheme": "Default Dark+",
        "codeEnabled": False,
        "systemLightTheme": "org.kde.breeze.desktop",
        "systemDarkTheme": "org.kde.breezedark.desktop",
        "systemEnabled": False,
        "gtkLightTheme": "",
        "gtkDarkTheme": "",
        "atomLightTheme": "",
        "atomDarkTheme": "",
        "atomEnabled": False,
        "gtkEnabled": False,
        "wallpaperLightTheme": "",
        "wallpaperDarkTheme": "",
        "wallpaperEnabled": False,
        "firefoxEnabled": False,
        "firefoxDarkTheme": "firefox-compact-dark@mozilla.org",
        "firefoxLightTheme": "firefox-compact-light@mozilla.org",
        "firefoxActiveTheme": "firefox-compact-light@mozilla.org",
        "kvantumEnabled": False,
        "kvantumLightTheme": "",
        "kvantumDarkTheme": "",
        "soundEnabled": False
    }
}


def use_all_versions(func):
    def inner(self):
        for version in old_configs:
            with self.subTest('Testing update from old version', version=version):
                old_config = old_configs[version]
                config.update(update_config(old_config.copy(), config.defaults))
                func(self, version, old_config)

    return inner


class ConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        config.reset()
        config.save()

    @use_all_versions
    def test_update_old_configs(self, version, old_config):
        match version:
            case 2.1:
                for plugin_property in ['Enabled', 'LightTheme', 'DarkTheme']:
                    self.assertEqual(
                        old_config['wallpaper' + plugin_property],
                        config.get_plugin_key(
                            'wallpaper',
                            plpr_str_to_enum(plugin_property.replace('Theme', '_theme').lower())),
                        'Updating old config files should apply correct values')
            case 2.2:
                self.assertEqual(config.mode, Modes.SCHEDULED)
                self.assertEqual(old_config['wallpaperEnabled'], config.get_plugin_key('wallpaper', PluginKey.ENABLED))
                self.assertEqual(old_config['wallpaperLightTheme'], config.get_plugin_key('wallpaper', PluginKey.THEME_LIGHT))

    @unittest.skipIf(config.desktop == Desktop.UNKNOWN, 'Desktop is unsupported')
    @use_all_versions
    def test_updates_system_plugin_values(self, version, old_config):
        match version:
            case 2.1:
                for plugin_property in ['Enabled', 'LightTheme', 'DarkTheme']:
                    self.assertEqual(
                        old_config['wallpaper' + plugin_property],
                        config.get_plugin_key(
                            'wallpaper',
                            plpr_str_to_enum(plugin_property.replace('Theme', '_theme').lower())),
                        'Updating old config files should apply correct values')

            case 2.2:
                self.assertEqual(config.mode, Modes.SCHEDULED)
                self.assertEqual(old_config['wallpaperEnabled'], config.get_plugin_key('wallpaper', PluginKey.ENABLED))
                self.assertEqual(old_config['wallpaperLightTheme'],
                                 config.get_plugin_key('wallpaper', PluginKey.THEME_LIGHT))

    def test_notifies_on_change(self):
        class Watcher(ConfigWatcher):
            def __init__(self):
                self.updates: [dict] = []

            def notify(self, event, values):
                self.updates.append(values)

        watcher = Watcher()
        config.add_event_listener(ConfigEvent.CHANGE, watcher)

        config.mode = Modes.SCHEDULED
        self.assertIn(
            {
                'key': 'mode',
                'old_value': Modes.MANUAL.value,
                'new_value': Modes.SCHEDULED.value,
                'plugin': None
            }, watcher.updates)
        watcher.updates = []

        config.add_event_listener(ConfigEvent.CHANGE, watcher)
        config.mode = Modes.MANUAL
        self.assertEqual(1, len(watcher.updates), 'Watcher should only be added once')

        config.mode = Modes.MANUAL
        self.assertNotIn(
            {
                'key': 'mode',
                'old_value': Modes.MANUAL.value,
                'new_value': Modes.MANUAL.value,
                'plugin': None
            }, watcher.updates)
        watcher.updates = []

        config.update_plugin_key('wallpaper', PluginKey.ENABLED, True)
        self.assertIn(
            {
                'key': PluginKey.ENABLED.value,
                'old_value': False,
                'new_value': True,
                'plugin': 'wallpaper'
            }, watcher.updates)
        watcher.updates = []

        try:
            config.update_plugin_key('abcd', PluginKey.ENABLED, True)
        except KeyError:
            pass
        self.assertTrue(len(watcher.updates) == 0)

    def test_removes_listener(self):
        class Watcher(ConfigWatcher):
            def __init__(self):
                self.notified = 0

            def notify(self, event: ConfigEvent, values: Optional[dict]):
                self.notified += 1

        watcher = Watcher()
        config.add_event_listener(ConfigEvent.CHANGE, watcher)
        config.mode = Modes.SCHEDULED
        config.remove_event_listener(ConfigEvent.CHANGE, watcher)
        config.mode = Modes.MANUAL
        self.assertEqual(1, watcher.notified)

    def test_notify_when_saved(self):
        class Watcher(ConfigWatcher):
            def __init__(self):
                self.saved = False

            def notify(self, event: ConfigEvent, values: dict):
                self.saved = True

        watcher = Watcher()
        config.add_event_listener(ConfigEvent.SAVE, watcher)
        self.assertFalse(watcher.saved)
        config.mode = Modes.SCHEDULED
        config.save()
        self.assertTrue(watcher.saved)

    def test_write_when_changed(self):
        self.assertFalse(config.save())

        config.mode = Modes.SCHEDULED
        self.assertTrue(config.save())
        self.assertFalse(config.save())

        config.update_plugin_key('wallpaper', PluginKey.ENABLED, True)
        self.assertTrue(config.save())
        self.assertFalse(config.save())

    def test_position(self):
        config.mode = Modes.FOLLOW_SUN
        config.update_location = True

        lat, long = config.location
        self.assertIsInstance(lat, float)
        self.assertIsInstance(long, float)

    def test_follow_sun(self):
        config.mode = Modes.SCHEDULED
        time_light_man = time(5, 9)
        time_dark_man = time(20, 0)
        config.times = time_light_man, time_dark_man

        config.mode = Modes.FOLLOW_SUN
        config.location = 0, 0
        time_light, time_dark = config.times

        self.assertNotEqual(time_light, time_light_man)
        self.assertNotEqual(time_dark, time_dark_man)

        config.update_location = True
        time_light, time_dark = config.times

        self.assertNotEqual(time_light, time_light_man)
        self.assertNotEqual(time_dark, time_dark_man)


def plpr_str_to_enum(string: str):
    """Returns the matching enum value from a plugin property string"""
    match string:
        case 'enabled':
            return PluginKey.ENABLED
        case 'dark_theme':
            return PluginKey.THEME_DARK
        case 'light_theme':
            return PluginKey.THEME_LIGHT


if __name__ == '__main__':
    unittest.main()
