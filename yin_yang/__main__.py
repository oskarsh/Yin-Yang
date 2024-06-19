#!/bin/env python3

import sys
import logging
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import QTranslator, QLibraryInfo, QLocale, QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from systemd import journal

from yin_yang.NotificationHandler import NotificationHandler
from yin_yang import daemon_handler
from yin_yang.meta import ConfigEvent
from yin_yang import theme_switcher
from yin_yang.config import config, Modes
from yin_yang.ui import main_window_connector

logger = logging.getLogger(__name__)


def setup_logger(use_systemd_journal: bool):
    notification_handler = NotificationHandler()
    notification_handler.addFilter(lambda record: record.levelno > logging.WARNING)
    logger.addHandler(notification_handler)

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


def systray_icon_clicked(reason: QSystemTrayIcon.ActivationReason):
    match reason:
        case QSystemTrayIcon.ActivationReason.MiddleClick:
            theme_switcher.set_mode(not config.dark_mode)
        case QSystemTrayIcon.ActivationReason.Trigger:
            window.show()


# using ArgumentParser for parsing arguments
parser = ArgumentParser()
parser.add_argument('-t', '--toggle',
                    help='toggles Yin-Yang',
                    action='store_true')
parser.add_argument('--systemd', help='uses systemd journal handler and applies desired theme', action='store_true')
parser.add_argument('--minimized', help='starts the program to tray bar', action='store_true')
arguments = parser.parse_args()
setup_logger(arguments.systemd)

if arguments.toggle:
    # terminate any running instances
    config.running = False
    config.mode = Modes.MANUAL
    theme_switcher.set_mode(not config.dark_mode)

elif arguments.systemd:
    theme_switcher.set_desired_theme()


else:
    # load GUI
    config.add_event_listener(ConfigEvent.SAVE, daemon_handler.watcher)
    config.add_event_listener(ConfigEvent.CHANGE, daemon_handler.watcher)
    app = QtWidgets.QApplication(sys.argv)
    # fixes icon on wayland
    app.setDesktopFileName('Yin-Yang')

    # load translation
    try:
        lang = QLocale().name()
        logger.debug(f'Using language {lang}')

        # system translations
        path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
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

    # show systray icon
    if QSystemTrayIcon.isSystemTrayAvailable():
        app.setQuitOnLastWindowClosed(False)

        icon = QSystemTrayIcon(QIcon(u':icons/logo'), app)
        icon.activated.connect(systray_icon_clicked)
        icon.setToolTip('Yin & Yang')

        menu = QMenu('Yin & Yang')
        menu.addAction(
            app.translate('systray', 'Open Yin Yang', 'Context menu action in the systray'),
            lambda: window.show())
        menu.addAction(
            app.translate('systray', 'Toggle theme', 'Context menu action in the systray'),
            lambda: theme_switcher.set_mode(not config.dark_mode))
        menu.addAction(QIcon.fromTheme('application-exit'),
                       app.translate('systray', 'Quit', 'Context menu action in the systray'),
                       app.quit)

        icon.setContextMenu(menu)
        icon.show()
    else:
        logger.debug('System tray is unsupported')

    if arguments.minimized:
        sys.exit(app.exec())
    else:
        window = main_window_connector.MainWindow()
        window.show()
        sys.exit(app.exec())
