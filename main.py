import sys
import logging
from argparse import ArgumentParser
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QTranslator

from src import yin_yang
from src import config
from src.ui import config_window

logger = logging.getLogger(__name__)

# fix HiDpi scaling
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)


def toggle_theme():
    """Switch themes"""
    theme = config.get_theme()
    if theme == "dark":
        yin_yang.switch_to_light()
    elif theme == "light":
        yin_yang.switch_to_dark()


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

    # checks whether $ yin-yang is ran without args
    if len(sys.argv) == 1 and not args.toggle:
        # load GUI
        app = QtWidgets.QApplication(sys.argv)

        # load translation
        try:
            translator = QTranslator()
            lang = QtCore.QLocale().name()
            logger.debug(f'Using language {lang}')
            if not translator.load(f'./resources/translations/yin_yang.{lang}.qm'):
                raise FileNotFoundError('Loading was not successful!')
            app.installTranslator(translator)
        except Exception as e:
            logger.error(str(e))
            print('Error while loading translation. Using default language.')

        window = config_window.MainWindow()
        window.show()
        sys.exit(app.exec_())

    # checks whether the script should be ran as a daemon
    if args.schedule:
        config.update("running", False)
        logger.debug("START thread listener")

        if config.get("followSun"):
            # calculate time if needed
            config.set_sun_time()

        if config.get("schedule"):
            yin_yang.start_daemon()
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
        config.update("running", False)
        config.update("followSun", False)
        config.update("schedule", False)
        toggle_theme()


if __name__ == "__main__":
    # __debug__ is true when you run main.py without the -O argument (python main.py)
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
