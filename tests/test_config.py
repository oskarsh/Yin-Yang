import json
import unittest
from pathlib import Path

from src.enums import Desktop, Modes
from src.config import config, get_desktop

config_path = f"{Path.home()}/.config/yin_yang/yin_yang_dev.json"

old_configs = {
    2.1: {
        "version": 2.1,
        "desktop": "kde",
        "followSun": False,
        "latitude": "",
        "longitude": "",
        "schedule": False,
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


def downgrade_config(old_config):
    with open(config_path, "w+") as file:
        json.dump(old_config, file)

    config.load()


class ConfigTest(unittest.TestCase):
    def test_update_old_configs(self):
        for version in [2.1, 2.2]:
            with self.subTest('Testing update from old version', version=version):
                old_config = old_configs[version]
                downgrade_config(old_config)

                if version == 2.1:
                    if get_desktop() != Desktop.UNKNOWN:
                        for plugin_property in ['Enabled', 'LightTheme', 'DarkTheme']:
                            self.assertEqual(
                                old_config[get_desktop().value + plugin_property],
                                config.get('system', plugin_property.replace('Theme', '_theme').lower()),
                                'Updating old config files should apply correct values')

                if version == 2.2:
                    self.assertEqual(config.mode, Modes.SCHEDULED)
                    self.assertEqual(old_config['systemEnabled'], config.get('system', 'enabled'))
                    self.assertEqual(old_config['systemLightTheme'], config.get('system', 'light_theme'))


if __name__ == '__main__':
    unittest.main()
