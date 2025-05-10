import json
import logging
import os
import pathlib
import shutil
from abc import ABC, abstractmethod
from datetime import time
from dateutil import tz
from functools import cache
from typing import Union, Optional

from psutil import process_iter, NoSuchProcess
from suntime import Sun, SunTimeException

from .position import get_current_location
from .meta import Modes, Desktop, PluginKey, ConfigEvent
from .plugins import get_plugins
from PySide6.QtCore import QStandardPaths

logger = logging.getLogger(__name__)

# aliases for path to use later on
config_path = pathlib.Path(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation))
if __debug__:
    config_path = config_path / 'yin_yang.json'
else:
    config_path = config_path / 'yin_yang_dev.json'


def update_config(config_old: dict, defaults: dict):
    """Update old config files
    Adds keys or restructures the config if an old config was loaded from the config file.
    Sets the new config directly to the dict in this class.

    :returns: the old config
    """

    logger.debug('Attempt to update the config file')

    # replace current config with defaults
    config_new = defaults

    # replace default values with previous ones
    if config_old['version'] <= 2.1:
        # Add or update keys to be compatible with the current version
        if "soundEnabled" not in defaults:
            config_old["soundEnabled"] = True

        name = "kde" if config_old["desktop"] == "kde" else "gnome"

        config_old['systemEnabled'] = config_old[f'{name}Enabled']
        config_old['systemLightTheme'] = config_old[f'{name}LightTheme']
        config_old['systemDarkTheme'] = config_old[f'{name}DarkTheme']

        # delete old keys
        for pl_old in ['kde', 'gnome']:
            for key in ['Enabled', 'LightTheme', 'DarkTheme']:
                config_old.pop(pl_old + key)

    if config_old['version'] <= 2.2:
        # determine mode
        if config_old.pop('followSun'):
            mode = Modes.FOLLOW_SUN.value
        elif config_old.pop('schedule'):
            mode = Modes.SCHEDULED.value
        else:
            mode = Modes.MANUAL.value
        config_new['mode'] = mode

        config_new['dark_mode'] = config_old.pop('theme') == 'dark'

        # put settings for PLUGINS into sections
        plugin_settings: dict = defaults['plugins']
        for plugin_name, plugin_config in plugin_settings.items():
            update_plugin_config(config_old, plugin_config, plugin_name)

    return config_new


def update_plugin_config(config_old, plugin_config, plugin_name):
    for key in plugin_config.keys():
        try:
            key_old = str(key).replace('_', ' ').title().replace(' ', '')
            # code was renamed to vs code
            match plugin_name:
                case 'vs code':
                    plugin_config[key] = config_old['code' + key_old]
                    continue
                case 'system':
                    plugin_config[key] = config_old[get_desktop().value + key_old]
                    continue
                case _:
                    plugin_config[key] = config_old[plugin_name.casefold() + key_old]
        except KeyError:
            if plugin_name == 'sound' and key in ['light_theme', 'dark_theme']:
                # this is expected since there is no theme
                continue
            logger.warning(f'Error while updating old config file. No value found for {plugin_name}.{key}')
            logger.info('This is most likely because the plugin was added in a later version')


@cache
def get_sun_time(latitude, longitude) -> tuple[time, time]:
    if latitude == longitude:
        logger.warning(f'Latitude and longitude are both {latitude}')
    else:
        logger.debug(f'Calculating sunset and sunrise at location {latitude}, {longitude}.')

    sun = Sun(latitude, longitude)
    local_tz = tz.gettz()
    try:
        today_sr = sun.get_sunrise_time(time_zone=local_tz)
        today_ss = sun.get_sunset_time(time_zone=local_tz)

        return today_sr.time(), today_ss.time()

    except SunTimeException as e:
        logger.error(f'Error: {e}.')


def get_desktop() -> Desktop:
    desktop = os.getenv('XDG_CURRENT_DESKTOP')
    if desktop is None:
        desktop = os.getenv('GDMSESSION')
    if desktop is None:
        desktop = ''

    match desktop.lower():
        case 'gnome':
            return Desktop.GNOME
        case 'kde' | 'plasma' | 'plasma5':
            return Desktop.KDE
        case 'xfce':
            return Desktop.XFCE
        case 'mate':
            return Desktop.MATE
        case 'x-cinnamon':
            return Desktop.CINNAMON
        case 'sway' | 'hyprland':
            return Desktop.GNOME
        case 'budgie:gnome' | 'budgie-desktop' | 'budgie':
            return Desktop.BUDGIE
        case _:
            return Desktop.UNKNOWN


plugins = get_plugins(get_desktop())


class ConfigWatcher(ABC):
    @abstractmethod
    def notify(self, event: ConfigEvent, values: Optional[dict]):
        raise NotImplementedError


class ConfigManager(dict):
    """Manages the configuration using the singleton pattern"""

    _listeners: dict[ConfigEvent, set[ConfigWatcher]] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(self.defaults)
        self._last_save_time = 0
        self._changed = False
        self.load()

    def add_event_listener(self, event: ConfigEvent, listener: ConfigWatcher):
        assert event == ConfigEvent.CHANGE or event == ConfigEvent.SAVE, 'enums are different!'

        if event not in self._listeners:
            self._listeners[event] = set()
        self._listeners[event].add(listener)

    def remove_event_listener(self, event: ConfigEvent, listener: ConfigWatcher):
        self._listeners[event].remove(listener)

    def __setitem__(self, key, value):
        if value == self[key]:
            return

        self._changed = True

        if ConfigEvent.CHANGE in self._listeners:
            for listener in self._listeners[ConfigEvent.CHANGE]:
                listener.notify(ConfigEvent.CHANGE, {
                    'key': key,
                    'old_value': self[key],
                    'new_value': value,
                    'plugin': None
                })

        super().__setitem__(key, value)

    def reset(self):
        """Resets all values to the defaults specified in the defaults' property."""

        logger.info('Setting default values.')
        self.update(self.defaults)
        self._changed = True

    def load(self) -> None:
        """Load config from file"""

        config_loaded = {}

        # change old config to new path
        old_path = pathlib.Path.home()
        old_file = old_path / 'yin_yang/config.json'
        if old_file.is_file():
            shutil.copyfile(old_file, config_path)
            os.remove(old_path)

        # check if conf exists
        if config_path.is_file():
            if self._last_save_time == config_path.stat().st_mtime:
                logger.debug('Loaded config file is up-to-date, skipping load')
                return

            # load conf
            logger.debug('Loading config file')
            with open(config_path, 'r') as config_file:
                config_loaded = json.load(config_file)
                self._last_save_time = config_path.stat().st_mtime

        if config_loaded is None or config_loaded == {}:
            # use default values if something went wrong
            logger.warning('Using default configuration values.')
            config_loaded = self.defaults

        # check if config needs an update
        # if the default values are set, the version number is below 0
        if float(config_loaded['version']) < self.defaults['version']:
            try:
                config_loaded = update_config(config_loaded, self.defaults)
            except Exception as e:
                logger.error('An error ocurred while trying to update the config. Using defaults instead.')
                logger.error(e)
                config_loaded = self.defaults

        for p in plugins:
            p.theme_light = config_loaded['plugins'][p.name.lower()]['light_theme']
            p.theme_dark = config_loaded['plugins'][p.name.lower()]['dark_theme']
            p.enabled = config_loaded['plugins'][p.name.lower()]['enabled']

        self.update(config_loaded)

    def save(self) -> bool:
        """Write configuration

        :returns: whether save was successful
        """

        if not self._changed:
            logger.debug('No changes were made, skipping save')
            return False

        logger.debug('Saving the config')
        try:
            with open(config_path, 'w') as conf_file:
                json.dump(self, conf_file, indent=4)
            # update time
            self._last_save_time = config_path.stat().st_mtime
            self._changed = False
            if ConfigEvent.SAVE in self._listeners:
                for listener in self._listeners[ConfigEvent.SAVE]:
                    listener.notify(ConfigEvent.SAVE, self)
            return True
        except IOError as e:
            logger.error(f'Error while writing the file: {e}')
            return False

    def get_plugin_key(self, plugin: str, key: PluginKey) -> Union[bool, str]:
        """Return the given key from the config
        :param plugin: name of the plugin
        :param key: the key to change
        :returns: value
        """

        plugin = plugin.casefold()
        key = key.value.casefold()

        return self['plugins'][plugin][key]

    def update_plugin_key(self, plugin_name: str, key: PluginKey, value: Union[bool, str]) -> Union[bool, str]:
        """Update the value of a key in configuration
        :param key: The setting to change
        :param value: The value to set the setting to
        :param plugin_name: Name of the plugin you may want to change

        :returns: new value
        """

        plugin_name_lower = plugin_name.casefold()
        key_value = key.value.casefold()

        try:
            old_value = self['plugins'][plugin_name_lower][key_value]
            if value == old_value:
                return value

            self['plugins'][plugin_name_lower][key_value] = value
            self._changed = True
            if ConfigEvent.CHANGE in self._listeners:
                for listener in self._listeners[ConfigEvent.CHANGE]:
                    listener.notify(ConfigEvent.CHANGE, {
                        'key': key_value,
                        'old_value': old_value,
                        'new_value': value,
                        'plugin': plugin_name_lower
                    })

            # change value in the plugin
            plugin = next(p for p in plugins if p.name.casefold() == plugin_name_lower)
            match key:
                case PluginKey.ENABLED:
                    plugin.enabled = value
                case PluginKey.THEME_LIGHT:
                    plugin.theme_light = value
                case PluginKey.THEME_DARK:
                    plugin.theme_dark = value
                case _:
                    raise KeyError

            return self.get_plugin_key(plugin_name_lower, key)
        except KeyError as e:
            logger.error(f'Error while updating {plugin_name_lower}.{key_value}')
            raise e

    @property
    def defaults(self) -> dict:
        """All default values"""

        # NOTE: if you change or add new values here, make sure to update the version number and update_config() method
        conf_default = {
            'version': 4.0,
            'running': False,
            'dark_mode': False,
            'mode': Modes.MANUAL.value,
            'coordinates': (0.0, 0.0),
            'update_location': False,
            'update_interval': 60,
            'times': ('07:00', '20:00'),
            'boot_offset': 10,
            'plugins': {}
        }

        # plugin settings
        for pl in plugins:
            conf_default['plugins'][pl.name.casefold()] = {
                'enabled': False,
                'light_theme': pl.theme_light,
                'dark_theme': pl.theme_dark
            }

        return conf_default

    @property
    def version(self) -> float:
        return self['version']

    @property
    def running(self) -> bool:
        """True, if yin yang is currently running"""

        # check if a process called yin_yang is running twice
        process_number = 0
        for process in process_iter():
            try:
                if 'yin_yang' in process.name():
                    process_number += 1
            except NoSuchProcess:
                pass
        return process_number > 1

    @running.setter
    def running(self, value: bool):
        self['running'] = value

    @property
    def dark_mode(self) -> bool:
        """Currently used theme. Might be wrong on initial start."""

        return self['dark_mode']

    @dark_mode.setter
    def dark_mode(self, dark_mode: bool):
        self['dark_mode'] = dark_mode
        self.save()

    @property
    def mode(self) -> Modes:
        """Mode that should be used to check whether dark mode should be active or not"""

        mode_string = self['mode']
        for mode in list(Modes):
            if mode_string == mode.value:
                return mode

        raise ValueError('Unsupported mode!')

    @mode.setter
    def mode(self, mode: Modes):
        self['mode'] = mode.value

    @property
    def location(self) -> tuple[float, float]:
        if self.update_location:
            try:
                coordinate = get_current_location()
                return coordinate.latitude(), coordinate.longitude()
            except TypeError as e:
                logger.error('Unable to update position. Using config values as fallback.')
                logger.error(e)
                pass
            except ValueError as e:
                logger.error('Unable to update position. Using config values as fallback.')
                logger.error(e)
                pass

        return self['coordinates']

    @location.setter
    def location(self, coordinates: tuple[float, float]):
        if self.update_location:
            raise ValueError('Location is updated automatically!')
        elif self.mode != Modes.FOLLOW_SUN:
            raise ValueError('Updating location while not in mode follow sun is forbidden')

        self['coordinates'] = coordinates

    @property
    def update_location(self) -> bool:
        """Whether the location should be updated automatically"""

        return self['update_location']

    @update_location.setter
    def update_location(self, enabled: bool):
        self['update_location'] = enabled

    @property
    def times(self) -> tuple[time, time]:
        """Times during which dark mode should be inactive"""

        if self.mode == Modes.FOLLOW_SUN:
            latitude, longitude = self.location
            return get_sun_time(latitude, longitude)

        # return time in config data
        time_light, time_dark = self['times']

        time_light = time.fromisoformat(time_light)
        time_dark = time.fromisoformat(time_dark)

        return time_light, time_dark

    @times.setter
    def times(self, times: tuple[time, time]):
        if self.mode != Modes.SCHEDULED:
            raise ValueError('Changing times is only allowed in mode scheduled!')

        self['times'] = times[0].isoformat(), times[1].isoformat()

    @property
    def desktop(self) -> Desktop:
        """Return the current desktops name or 'unknown' if it can't determine it"""

        return get_desktop()

    @property
    def boot_offset(self) -> int:
        """Seconds that should pass until next check"""

        return self['boot_offset']

    @boot_offset.setter
    def boot_offset(self, value: int):
        self['boot_offset'] = value


# create global object with current version
# NOTE change the version here if the structure of the config file has been modified
config = ConfigManager()

logger.info('Detected desktop:', config.desktop)

# set plugin themes
for pl in filter(lambda pl: pl.available, plugins):
    pl.enabled = config.get_plugin_key(pl.name, PluginKey.ENABLED)
    pl.theme_bright = config.get_plugin_key(pl.name, PluginKey.THEME_LIGHT)
    pl.theme_dark = config.get_plugin_key(pl.name, PluginKey.THEME_DARK)
