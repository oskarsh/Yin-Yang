
"""
title: yin_yang
description: yin_yang provides a easy way to toggle between light and dark
mode for your kde desktop. It also themes your vscode and
all other qt application with it.
author: oskarsh
date: 21.12.2018
license: MIT
"""

import logging
import time
from datetime import datetime

from src.config import Modes, config, plugins

logger = logging.getLogger(__name__)


def should_be_dark(time_current: time, time_light: time, time_dark: time) -> bool:
    """Compares two times with current time"""

    if time_light < time_dark:
        return not (time_light <= time_current < time_dark)
    else:
        return time_dark <= time_current < time_light


def set_mode(dark: bool):
    """Activates light or dark theme"""

    if dark == config.dark_mode:
        return

    logger.info(f'Switching to {"dark" if dark else "light"} mode.')
    for p in plugins:
        if config.get(p.name, 'enabled'):
            try:
                p.set_mode(dark)
            except Exception as e:
                logger.error('Error while changing theme in ' + p.name, exc_info=e)

    config.dark_mode = dark


def run():
    logger.info(f'System is currently using a {"dark" if config.dark_mode else "light"} theme.')
    while config.mode != Modes.manual:
        # load settings if something has changed
        config.load()
        time_light, time_dark = config.times
        set_mode(should_be_dark(datetime.now().time(), time_light, time_dark))
        # subtract seconds so that the next switch is on the full minute
        time.sleep(config.update_interval - datetime.now().second)
