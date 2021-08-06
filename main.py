import sys
import logging
from argparse import ArgumentParser
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from src import yin_yang
from src import config
from src import gui

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
        window = gui.MainWindow()
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
    # __debug__ is true when main.py is run without the -O argument.
    if __debug__:
        # noinspection SpellCheckingInspection
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s - %(name)s: %(message)s'
        )
    else:
        # logger to see what happens when application is running in background
        # noinspection SpellCheckingInspection
        logging.basicConfig(
            filename=str(Path.home()) + '/.local/share/yin_yang.log',
            level=logging.WARNING,
            format='%(asctime)s %(levelname)s - %(name)s: %(message)s'
        )
    main()
