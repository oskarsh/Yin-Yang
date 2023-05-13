#!/bin/env python3

import sys
import logging
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import QTranslator, QLibraryInfo, QLocale
from systemd import journal

from yin_yang import daemon_handler
from yin_yang.meta import ConfigEvent
from yin_yang import theme_switcher
from yin_yang.config import config, Modes
from yin_yang.ui import main_window_connector

logger = logging.getLogger()


def setup_logger(use_systemd_journal: bool):
    if use_systemd_journal:
        logger.addHandler(journal.JournalHandler(SYSLOG_IDENTIFIER='yin_yang'))

    # __debug__ is true when you run __main__.py without the -O argument (python __main__.py)
    # noinspection PyUnreachableCode
    if __debug__:
        # noinspection SpellCheckingInspection
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s - %(name)s: %(message)s'
        )
    else:
        # if you run it with "python -O __main__.py" instead, debug is false

        # let the default logger print to the console
        # noinspection SpellCheckingInspection
        logging.basicConfig(
            level=logging.WARNING,
            format='%(asctime)s %(levelname)s - %(name)s: %(message)s'
        )
        # and add a handler that limits the size to 1 GB
        file_handler = RotatingFileHandler(
            str(Path.home()) + '/.local/share/yin_yang.log',
            maxBytes=10**9, backupCount=1
        )
        logging.root.addHandler(file_handler)


# using ArgumentParser for parsing arguments
parser = ArgumentParser()
parser.add_argument("-t", "--toggle",
                    help="toggles Yin-Yang",
                    action="store_true")
parser.add_argument("--systemd", help="uses systemd journal handler and applies desired theme", action='store_true')
arguments = parser.parse_args()
setup_logger(arguments.systemd)

# checks whether $ yin-yang is run without args
if len(sys.argv) == 1:
    config.add_event_listener(ConfigEvent.SAVE, daemon_handler.watcher)
    config.add_event_listener(ConfigEvent.CHANGE, daemon_handler.watcher)
    # load GUI
    app = QtWidgets.QApplication(sys.argv)

    # load translation
    try:
        lang = QLocale().name()
        logger.debug(f'Using language {lang}')

        # system translations
        path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)
        translator = QTranslator(app)
        if translator.load(QLocale.system(), 'qtbase', '_', path):
            app.installTranslator(translator)
        else:
            raise FileNotFoundError('Error while loading system translations!')

        # application translations
        translator = QTranslator(app)
        path = ':translations'
        if translator.load(QLocale.system(), 'yin_yang', '.', path):
            app.installTranslator(translator)
        else:
            raise FileNotFoundError('Error while loading application translations!')

    except Exception as e:
        logger.error(str(e))
        print('Error while loading translation. Using default language.')

    window = main_window_connector.MainWindow()
    window.show()
    sys.exit(app.exec())

if arguments.toggle:
    # terminate any running instances
    config.running = False
    config.mode = Modes.MANUAL
    theme_switcher.set_mode(not config.dark_mode)

if arguments.systemd:
    theme_switcher.set_desired_theme()