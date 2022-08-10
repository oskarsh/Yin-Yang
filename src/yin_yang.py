#!/bin/python


"""
title: yin_yang
description: yin_yang provides a easy way to toggle between light and dark
mode for your kde desktop. It also themes your vscode and
all other qt application with it.
author: oskarsh
date: 21.12.2018
license: MIT
"""

import datetime
import logging
import os
import pwd
import subprocess
import sys
import threading
import time
import traceback

from src.config import config
from src.plugins import get_plugins, ExternalPlugin

logger = logging.getLogger(__name__)
plugins = get_plugins(config.desktop)

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/" + user + "/.config/"

terminate = False


class Yang(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        for pl in plugins:
            if isinstance(pl, ExternalPlugin):
                continue

            if pl.enabled:
                logger.info('Changing theme in plugin ' + pl.name)
                try:
                    if not pl.set_mode(False):
                        raise ValueError('set_mode() did not return True.')
                except Exception as e:
                    logger.error('Error while changing the theme in plugin ' + pl.name)
                    traceback.print_exception(type(e), e, e.__traceback__)
        play_sound("./assets/light.wav")


class Yin(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        for pl in plugins:
            if isinstance(pl, ExternalPlugin):
                continue

            if pl.enabled:
                logger.info('Changing theme in plugin ' + pl.name)
                try:
                    if not pl.set_mode(True):
                        raise ValueError('set_mode() did not return True.')
                except Exception as e:
                    logger.error('Error while changing the theme in plugin ' + pl.name)
                    traceback.print_exception(type(e), e, e.__traceback__)
        play_sound("./assets/dark.wav")


class Daemon(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        while True:

            if terminate:
                config.update("running", False)
                break

            if not config.is_scheduled():
                config.update("running", False)
                break

            editable = config.get_config()

            theme = config.get("theme")

            if should_be_light():
                if theme == "light":
                    time.sleep(30)
                    continue
                else:
                    switch_to_light()
            else:
                if theme == "dark":
                    time.sleep(30)
                    continue
                else:
                    switch_to_dark()

            time.sleep(30)


def switch_to_light():
    yang = Yang(1)
    yang.start()
    config.update("theme", "light")
    yang.join()


def switch_to_dark():
    yin = Yin(2)
    yin.start()
    config.update("theme", "dark")
    yin.join()


def start_daemon():
    daemon = Daemon(3)
    daemon.start()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def play_sound(sound):
    """ Description - only works with pulseaudio.
    :type sound: String (Path)
    :param sound: Sound path to be played audio file from
    :rtype: I hope you will hear your Sound ;)
    """

    if config.sound_get_checkbox():
        subprocess.run(["paplay", resource_path(sound)])


def should_be_light():
    # desc: return if the Theme should be light
    # returns: True if it should be light
    # returns: False if the theme should be dark

    time_light, time_dark = config.times
    time_current = datetime.datetime.now().time()

    if time_light < time_dark:
        return time_light <= time_current < time_dark
    else:
        return not (time_dark <= time_current < time_light)
