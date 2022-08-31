import json
import logging
import os
import pathlib
import re
from functools import cache
from psutil import process_iter, NoSuchProcess
from datetime import time
from enum import Enum
from typing import Union

import requests
from suntime import Sun, SunTimeException
from src.plugins import get_plugins

logger = logging.getLogger(__name__)


class Modes(Enum):
    """Different modes for determining the theme that should be used"""

    manual = 'manual'
    scheduled = 'manual time'
    followSun = 'sunset to sunrise'


# aliases for path to use later on
home = str(pathlib.Path.home())
config_path = home + '/.config/yin_yang/yin_yang.json'


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
        # determine mode
        if config_old.pop('schedule'):
            mode = Modes.scheduled.value
        elif config_old.pop('followSun'):
            mode = Modes.followSun.value
        else:
            mode = Modes.manual.value
        config_new['mode'] = mode

        config_new['dark_mode'] = config_old.pop('theme') == 'dark'

        # put settings for PLUGINS into sections
        plugin_settings: dict = defaults['plugins']
        for plugin_name, plugin_config in plugin_settings.items():
            for key in plugin_config.keys():
                try:
                    key_old = str(key).replace('_', ' ').title().replace(' ', '')
                    # code was renamed to vs code
                    if plugin_name == 'vs code':
                        plugin_config[key] = config_old['code' + key_old]
                        continue
                    if plugin_name == 'system':
                        plugin_config[key] = config_old[get_desktop() + key_old]
                        continue
                    plugin_config[key] = config_old[plugin_name.casefold() + key_old]
                except KeyError:
                    if plugin_name == 'sound' and key in ['light_theme', 'dark_theme']:
                        # this is expected since there is no theme
                        continue
                    logger.warning(f'Error while updating old config file. No value found for {plugin_name}.{key}')
                    logger.info('This is most likely because the plugin was added in a later version')
    return config_new


@cache
def get_sun_time(latitude, longitude) -> tuple[time, time]:
    if latitude == longitude:
        logger.warning(f'Latitude and longitude are both {latitude}')
    else:
        logger.debug(f'Calculating sunset and sunrise at location {latitude}, {longitude}.')

    sun = Sun(latitude, longitude)
    try:
        today_sr = sun.get_local_sunrise_time()
        today_ss = sun.get_local_sunset_time()

        return today_sr.time(), today_ss.time()

    except SunTimeException as e:
        logger.error(f'Error: {e}.')


@cache
def get_current_location() -> tuple[float, float]:
    logger.debug('Updating location.')
    loc_response = requests.get('https://www.ipinfo.io/loc').text.split(',')
    # convert the strings to floats
    loc: [float] = [float(coordinate) for coordinate in loc_response]
    assert len(loc) == 2, 'The returned location should have exactly 2 values.'
    return loc[0], loc[1]


def get_desktop() -> str:
    # just to get all possible implementations of desktop variables
    # noinspection SpellCheckingInspection
    env = str(os.getenv('GDMSESSION')).lower()
    second_env = str(os.getenv('XDG_CURRENT_DESKTOP')).lower()
    third_env = str(os.getenv('XDG_CURRENT_DESKTOP')).lower()

    # these are the envs I will look for
    # feel free to add your Desktop and see if it works
    gnome_re = re.compile(r'gnome')
    budgie_re = re.compile(r'budgie')
    kde_re = re.compile(r'kde')
    plasma_re = re.compile(r'plasma')
    plasma5_re = re.compile(r'plasma5')

    if (gnome_re.search(env) or
            gnome_re.search(second_env) or gnome_re.search(third_env)):
        return 'gtk'
    if (budgie_re.search(env) or
            budgie_re.search(second_env) or budgie_re.search(third_env)):
        return 'gtk'
    if (kde_re.search(env) or
            kde_re.search(second_env) or kde_re.search(third_env)):
        return 'kde'
    if (plasma_re.search(env) or
            plasma_re.search(second_env) or plasma_re.search(third_env)):
        return 'kde'
    if (plasma5_re.search(env) or
            plasma5_re.search(second_env) or plasma5_re.search(third_env)):
        return 'kde'
    return 'unknown'


plugins = get_plugins(get_desktop())


class ConfigManager:
    """Manages the configuration using the singleton pattern"""

    _config_data: dict = None

    def __init__(self):
        self._config_data = self.defaults
        self._last_save_time = 0
        self._changed = False
        self.load()

    def set_default(self):
        """Resets all values to the defaults specified in the defaults property."""

        logger.info('Setting default values.')
        self._config_data = self.defaults
        self._changed = True

    def load(self) -> None:
        """Load config from file"""

        # generate path for yin-yang if there is none this will be skipped
        pathlib.Path(home + '/.config/yin_yang').mkdir(parents=True, exist_ok=True)

        config_loaded = {}

        # check if conf exists
        if os.path.isfile(config_path):
            if self._last_save_time == os.stat(config_path).st_mtime:
                logger.debug('Loaded config file is up-to-date, skipping load')
                return

            # load conf
            logger.debug('Loading config file')
            with open(config_path, 'r') as config_file:
                config_loaded = json.load(config_file)
                self._last_save_time = os.stat(config_path).st_mtime

        if config_loaded is None or config_loaded == {}:
            # use default values if something went wrong
            logger.warning('Using default configuration values.')
            config_loaded = self.defaults

        # check if config needs an update
        # if the default values are set, the version number is below 0
        if config_loaded['version'] < self.defaults['version']:
            config_loaded = update_config(config_loaded, self.defaults)

        for pl in plugins:
            pl.theme_light = config_loaded['plugins'][pl.name.lower()]['light_theme']
            pl.theme_dark = config_loaded['plugins'][pl.name.lower()]['dark_theme']
            pl.enabled = config_loaded['plugins'][pl.name.lower()]['enabled']

        self._config_data = config_loaded

    def write(self) -> bool:
        """Write configuration

        :returns: whether save was successful
        """

        if not self._changed:
            logger.debug('No changes were made, skipping save')
            return True

        logger.debug('Saving the config')
        try:
            with open(config_path, 'w') as conf_file:
                json.dump(self._config_data, conf_file, indent=4)
            # update time
            self._last_save_time = os.stat(config_path).st_mtime
            return True
        except IOError as e:
            logger.error(f'Error while writing the file: {e}')
            return False

    def get(self, plugin: str, key: str) -> Union[bool, str]:
        """Return the given key from the config
        :param plugin: name of the plugin
        :param key: the key to change
        :returns: value
        """

        plugin = plugin.casefold()
        key = key.casefold()

        return self._config_data['plugins'][plugin][key]

    def update(self, plugin: str, key: str, value: Union[bool, str]) -> Union[bool, str]:
        """Update the value of a key in configuration

        :param key: The setting to change
        :param value: The value to set the setting to
        :param plugin: Name of the plugin you may want to change

        :returns: new value
        """

        plugin = plugin.casefold()
        key = key.casefold()

        try:
            self._config_data['plugins'][plugin][key] = value
            self._changed = True
            return self.get(plugin, key)
        except KeyError as e:
            logger.error(f'Error while updating {plugin}.{key}')
            raise e

    @property
    def defaults(self) -> dict:
        """All default values"""

        # NOTE: if you change or add new values here, make sure to update the version number and update_config() method
        conf_default = {
            'version': 2.3,
            'running': False,
            'dark_mode': False,
            'mode': Modes.manual.value,
            'coordinates': (0, 0),
            'update_location': False,
            'update_interval': 60,
            'times': ('07:00', '20:00'),
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
    def data(self) -> dict:
        """All config values. Only use this for testing purposes!"""

        return self._config_data

    @property
    def version(self) -> float:
        return self._config_data['version']

    @property
    def running(self) -> bool:
        """True, if yin yang is currently running"""

        # check if a process called yin_yang is running twice
        process_number = 0
        for process in process_iter():
            try:
                if 'yin-yang' in process.name():
                    process_number += 1
            except NoSuchProcess:
                pass
        return process_number > 1

    @running.setter
    def running(self, value: bool):
        self._config_data['running'] = value
        self._changed = True

    @property
    def dark_mode(self) -> bool:
        """Currently used theme. Might be wrong on initial start."""

        return self._config_data['dark_mode']

    @dark_mode.setter
    def dark_mode(self, dark_mode: bool):
        self._config_data['dark_mode'] = dark_mode
        self._changed = True
        self.write()

    @property
    def mode(self) -> Modes:
        """Mode that should be used to check wether dark mode should be active or not"""

        mode_string = self._config_data['mode']
        for mode in list(Modes):
            if mode_string == mode.value:
                return mode

        raise ValueError('Unsupported mode!')

    @mode.setter
    def mode(self, mode: Modes):
        self._config_data['mode'] = mode.value
        self._changed = True

    @property
    def location(self) -> tuple[float, float]:
        if self._config_data['update_location']:
            try:
                return get_current_location()
            except requests.exceptions.ConnectionError as e:
                logger.warning('Could not update location. Please check your internet connection.')
                logger.error(str(e))

        return self._config_data['coordinates']

    @location.setter
    def location(self, coordinates: tuple[float, float]):
        if self._config_data['update_location']:
            raise ValueError('Location is updated automatically!')
        elif self.mode != Modes.followSun:
            raise ValueError('Updating location while not in mode follow sun is forbidden')

        self._config_data['coordinates'] = coordinates
        self._changed = True

    @property
    def update_location(self) -> bool:
        """Wether the location should be updated automatically"""

        return self._config_data['update_location']

    @update_location.setter
    def update_location(self, enabled: bool):
        self._config_data['update_location'] = enabled
        self._changed = True

    @property
    def times(self) -> tuple[time, time]:
        """Times during which dark mode should be inactive"""

        if self.mode == Modes.followSun:
            latitude, longitude = self.location
            return get_sun_time(latitude, longitude)

        # return time in config data
        time_light, time_dark = self._config_data['times']

        time_light = time.fromisoformat(time_light)
        time_dark = time.fromisoformat(time_dark)

        return time_light, time_dark

    @times.setter
    def times(self, times: tuple[time, time]):
        if self.mode == Modes.scheduled:
            self._config_data['times'] = times[0].isoformat(), times[1].isoformat()
            self._changed = True
        else:
            raise ValueError('Changing times is only allowed in mode scheduled!')

    @property
    def desktop(self) -> str:
        """Return the current desktops name or 'unknown' if can't determine it"""

        return get_desktop()

    @property
    def update_interval(self) -> int:
        """Seconds that should pass until next check"""

        return self._config_data['update_interval']


# create global object with current version
# NOTE change the version here if the structure of the config file has been modified
config = ConfigManager()

logger.info('Detected desktop:', config.desktop)

# set plugin themes
for p in filter(lambda pl: pl.available, plugins):
    p.enabled = config.get(p.name, 'enabled')
    p.theme_bright = config.get(p.name, 'light_theme')
    p.theme_dark = config.get(p.name, 'dark_theme')
