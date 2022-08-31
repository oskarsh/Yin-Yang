#!/bin/env python3

import sys
import logging
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import QTranslator, QLibraryInfo, QLocale

from src import yin_yang
from src.config import config, Modes
from src.ui import config_window

logger = logging.getLogger(__name__)


def main():
    # using ArgumentParser for parsing arguments
    parser = ArgumentParser()
    parser.add_argument("-t", "--toggle",
                        help="toggles Yin-Yang",
                        action="store_true")
    parser.add_argument("-s", "--schedule",
                        help="schedule theme toggle, starts daemon in bg",
                        action="store_true")
    args = parser.parse_args()

    # checks whether $ yin-yang is run without args
    if len(sys.argv) == 1 and not args.toggle:
        # load GUI
        app = QtWidgets.QApplication(sys.argv)

        # load translation
        try:
            lang = QLocale().name()
            logger.debug(f'Using language {lang}')

            # system translations
            path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
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

        window = config_window.MainWindow()
        window.show()
        sys.exit(app.exec())

    # checks whether the script should be run as a daemon
    if args.schedule:
        config.running = False

        if config.mode != Modes.manual:
            yin_yang.run()
        else:
            logger.warning("Tried to start scheduler, but schedule was not enabled.")
            print(
                "Looks like you have not specified a time."
                "You can use the GUI by running Yin & Yang or "
                "edit the config found in ~/.config/yin_yang/yin_yang.json."
                "You need to set schedule to true and edit the time to toggles."
            )

    if args.toggle:
        # terminate any running instances
        config.running = False
        config.mode = Modes.manual
        yin_yang.set_mode(not config.dark_mode)


if __name__ == "__main__":
    # __debug__ is true when you run main.py without the -O argument (python main.py)
    # noinspection PyUnreachableCode
    if __debug__:
        # noinspection SpellCheckingInspection
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s - %(name)s: %(message)s'
        )
    else:
        # if you run it with "python -O main.py" instead, debug is false

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
    main()
