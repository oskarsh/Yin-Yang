import sys
from argparse import ArgumentParser
from src import yin_yang
from src import config
from src import gui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

assembly_version = 2.1

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

    # Check and see if there are new keys we need to add to the config.
    should_update_config = assembly_version != config.get_version()
    if should_update_config:
        update_config()

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
        print("START thread listener")

        if config.get("followSun"):
            # calculate time if needed
            config.set_sun_time()

        if config.get("schedule"):
            yin_yang.start_daemon()
        else:
            print("looks like you did not specified a time")
            print("You can use the gui with yin-yang -gui")
            print("Or edit the config found in ~/.config/yin_yang/yin_yang.json")
            print("You need to set schedule to True and edit the time to toggles")

    # gui is set as parameter
    if args.toggle:
        toggle_theme()


# This method is called to add keys to the config
# which have been added since version 1.0
def update_config():
    if "soundEnabled" not in config.config:
        config.config["soundEnabled"] = True

    config.update("version", assembly_version)


if __name__ == "__main__":
    main()
