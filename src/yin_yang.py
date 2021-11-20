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
import dbus

import src.yin_yang
from src import config
from src.plugins import plugins

logger = logging.getLogger(__name__)

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
            if isinstance(pl, src.plugins.ExternalPlugin):
                continue

            if pl.enabled:
                logger.info('Changing theme in plugin ' + pl.name)
                try:
                    if not pl.set_mode(False):
                        raise ValueError('set_mode() did not return True.')
                except Exception as e:
                    logger.error('Error while changing the theme in plugin ' + pl.name)
                    traceback.print_exception(type(e), e, e.__traceback__)
        os_notificate("Theme changed to light")


class Yin(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        for pl in plugins:
            if isinstance(pl, src.plugins.ExternalPlugin):
                continue

            if pl.enabled:
                logger.info('Changing theme in plugin ' + pl.name)
                try:
                    if not pl.set_mode(True):
                        raise ValueError('set_mode() did not return True.')
                except Exception as e:
                    logger.error('Error while changing the theme in plugin ' + pl.name)
                    traceback.print_exception(type(e), e, e.__traceback__)
        os_notificate("Theme changed to dark")


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

def os_notificate(message: str):
    session = dbus.SessionBus()
    notify_proxy = session.get_object(
        'org.freedesktop.Notifications',
        '/org/freedesktop/Notifications'
    )

    notify_proxy.Notify(
        'Yin & Yang', 
        0, 
        '', 
        message, 
        '', 
        [], 
        [], 
        5000, 
        dbus_interface="org.freedesktop.Notifications"
    )

def should_be_light():
    # desc: return if the Theme should be light
    # returns: True if it should be light
    # returns: False if the theme should be dark

    d_hour = int(config.get("switchToDark").split(":")[0])
    d_minute = int(config.get("switchToDark").split(":")[1])
    l_hour = int(config.get("switchToLight").split(":")[0])
    l_minute = int(config.get("switchToLight").split(":")[1])
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute

    # if light comes before dark (True if 00:00 -> light -> dark -> 23:59)
    if l_hour < d_hour or (l_hour == d_hour and l_minute < d_minute):
        if hour >= l_hour and hour < d_hour:
            return not (hour == l_hour and minute <= l_minute)
        else:
            return hour == d_hour and minute <= d_minute
    else:
        # same as above, but checks for dark and inverts the result
        if hour >= d_hour and hour < l_hour:
            return hour == d_hour and minute <= d_minute
        else:
            return not (hour == l_hour and minute <= l_minute)
