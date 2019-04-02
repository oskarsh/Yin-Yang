import sys
from argparse import ArgumentParser
from src import yin_yang
from src import config
from src import gui
from PyQt5 import QtWidgets


def toggleTheme():
    theme = config.getTheme()
    if (theme == "dark"):
        yin_yang.switchToLight()
    elif (theme == "light"):
        yin_yang.switchToDark()


def main():
    # using ArgumentParser for parsing arguments
    parser = ArgumentParser()
    parser.add_argument("-gui", "--gui",
                        help="opens Yin-Yang as a GUI application",
                        action="store_true")
    parser.add_argument("-s", "--schedule",
                        help="schedule theme toggl, starts daemon in bg",
                        action="store_true")
    args = parser.parse_args()

    # checks wether $ yin-yang is ran without args
    if (len(sys.argv) == 1 and not args.gui):
        toggleTheme()

    # checks wether the script should be ran as a daemon
    if (args.schedule):
        config.update("running", False)
        print("START thread listener")
        if config.get("schedule"):
            yin_yang.startDaemon()
        else:
            print("looks like you did not specified a time")
            print("You can use the gui with yin-yang -gui")
            print("Or edit the config found in ~/.config/yin_yang/yin_yang.json")
            print("You need to set schedule to True and edit the time to toggles")

    # gui is set as parameter
    if (args.gui):
        # load GUI
        app = QtWidgets.QApplication(sys.argv)
        window = gui.MainWindow()
        window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
