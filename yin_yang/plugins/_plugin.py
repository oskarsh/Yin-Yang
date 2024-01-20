import copy
import logging
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from PySide6.QtDBus import QDBusConnection, QDBusMessage
from PySide6.QtGui import QColor, QRgba64
from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLineEdit, QComboBox

from ..meta import UnsupportedDesktopError

logger = logging.getLogger(__name__)


class Plugin(ABC):
    """An abstract base class for plugins"""

    def __init__(self):
        self.enabled = False
        self.theme_light = ''
        self.theme_dark = ''

    @property
    def name(self) -> str:
        """Returns a readable name of the plugin"""
        return type(self).__name__

    @property
    def available(self) -> bool:
        """Check whether a plugin is available
        For example, if VS Code is not installed, the plugin vscode is not available
        :return: true, if the theme can be set
        """
        return True

    @property
    def available_themes(self) -> dict:
        """Return a list of available themes
        :return: Dict[intern_name, readable_name]
        """
        return {}

    def set_mode(self, dark: bool) -> bool:
        """Set the dark or light theme
        :return: True, if operation was successful
        """

        if not self.enabled:
            return False

        theme = self.theme_dark if dark else self.theme_light
        self.set_theme(theme)
        return True

    @abstractmethod
    def set_theme(self, theme: str):
        """Sets a specific theme
        :param theme: the theme that should be used
        :return: the theme that has been set (should be the same as the parameter
        """
        raise NotImplementedError

    def get_widget(self, area) -> QGroupBox:
        """Returns a widget for the settings menu
        area: scrollAreaWidgetContents
        """

        widget = QGroupBox(area)
        widget.setTitle(self.name)
        widget.setCheckable(True)
        widget.setChecked(self.enabled)
        widget.setVisible(self.available)
        widget.setObjectName('group' + self.name)

        horizontal_layout = QHBoxLayout(widget)

        for inp in self.get_input(widget):
            horizontal_layout.addWidget(inp)

        return widget

    def get_input(self, widget):
        """Returns two inputs for dark and light theme for the config gui"""
        inputs = []

        if self.available_themes != {}:
            # use a combobox if the possible themes are known
            inputs = [QComboBox(widget), QComboBox(widget)]

            # add all theme names
            for i, curComboBox in enumerate(inputs):
                themes = list(self.available_themes.values())
                themes.sort(key=lambda s: s.casefold())
                curComboBox.addItems(themes)
                curComboBox.setMinimumContentsLength(4)
                # set index
                is_dark = i == 1
                theme: str = self.theme_dark if is_dark else self.theme_light
                try:
                    curComboBox.setCurrentIndex(themes.index(self.available_themes[theme]))
                except (KeyError, ValueError):
                    logger.warning(f'Couldn\'t find theme {theme} in plugin {self.name}')
                    curComboBox.setCurrentIndex(0)
            return inputs
        else:
            for is_dark in [False, True]:
                theme = 'Dark' if is_dark else 'Light'
                # provide a line edit, if the possible themes are unknown
                inp: QLineEdit = QLineEdit(widget)
                inp.setObjectName(f'inp_{theme}')
                inp.setPlaceholderText(f'{theme} Theme')
                inp.setText(self.theme_dark if is_dark else self.theme_light)
                inputs.append(inp)

            return inputs

    def __str__(self):
        return self.name.lower()


class PluginCommandline(Plugin):
    def __init__(self, command: list[str]):
        """
        :param command: list of arguments as passed to @subprocess.run, with the theme being inserted as {theme}
        """
        super().__init__()
        self.command = command

    def set_theme(self, theme: str):
        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        if not (self.available and self.enabled):
            return

        # insert theme in command and run it
        command = self.insert_theme(theme)
        subprocess.check_call(command)

    def insert_theme(self, theme: str) -> list:
        command = self.command.copy()

        for i, arg in enumerate(command):
            command[i] = arg.format(theme=theme)

        return command

    @staticmethod
    def check_command(command) -> bool:
        # Returns true if command execution succeeds
        try:
            subprocess.check_call(command, stdout=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            # if no such command is available, the plugin is not available
            return False
        except subprocess.CalledProcessError:
            # command execution failed
            return False

    @property
    def available(self):
        return self.check_command([self.command[0], '--help'])


class PluginDesktopDependent(Plugin):
    """Plugins that behave differently on different desktops"""

    def __init__(self, strategy_instance: Optional[Plugin]):
        self._strategy_instance = None
        super().__init__()
        self._strategy_instance = strategy_instance

        if strategy_instance is None:
            logger.warning(f'Plugin {self.name} has no support for your desktop environment yet!')

    @property
    def strategy(self) -> Plugin | None:
        return self._strategy_instance

    @property
    def enabled(self):
        return self.strategy.enabled if self.strategy is not None else False

    @enabled.setter
    def enabled(self, value):
        if self.strategy is not None:
            self.strategy.enabled = value

    @property
    def available(self) -> bool:
        return False if self.strategy is None else self.strategy.available

    def set_theme(self, theme: str):
        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        if not (self.available and self.enabled):
            return

        if self.strategy is None:
            raise UnsupportedDesktopError

        self.strategy.set_theme(theme)

    @property
    def available_themes(self) -> dict:
        if self.strategy is not None:
            return self.strategy.available_themes
        return {}

    @property
    def theme_light(self):
        if self.strategy is not None:
            return self.strategy.theme_light
        return ''

    @theme_light.setter
    def theme_light(self, value):
        if self.strategy is not None:
            self.strategy.theme_light = value

    @property
    def theme_dark(self):
        if self.strategy is not None:
            return self.strategy.theme_dark
        return ''

    @theme_dark.setter
    def theme_dark(self, value):
        if self.strategy is not None:
            self.strategy.theme_dark = value


class ExternalPlugin(Plugin):
    """A class for all plugins whose theme can only be changed externally via communication."""

    def __init__(self, url):
        super().__init__()
        self._url = url

    @property
    def url(self) -> str:
        return ('Please remember to install the plugin.\n'
                f'You can get it here: {self._url}')

    def set_theme(self, theme: str):
        # throws error if in debug mode, else ignored
        assert False, 'This is an external plugin, the mode can only be changed externally.'


class DBusPlugin(Plugin):
    def __init__(self, base_message: QDBusMessage):
        super().__init__()
        self.connection = QDBusConnection.sessionBus()
        self.base_message = base_message

    def set_theme(self, theme: str):
        self.call(self.create_message(theme))

    def create_message(self, theme: str) -> QDBusMessage:
        message = copy.deepcopy(self.base_message)
        message.setArguments([theme])
        return message

    def call(self, message) -> QDBusMessage:
        return self.connection.call(message)


def inplace_change(filename: str | Path, old_string: str, new_string: str):
    """Replaces a given string by a new string in a specific file
    :param filename: the full path to the file that should be changed
    :param old_string: the old string that should be found in the file
    :param new_string: the string that should replace the old string
    """
    # Safely read the input filename using 'with'
    with open(filename, 'r') as file:
        file_content = file.read()
        if old_string not in file_content:
            raise ValueError(f'{old_string} could not be found in {filename}')

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as file:
        file_content = file_content.replace(old_string, new_string)
        file.write(file_content)


def get_qcolor_from_int(color_int: int) -> QColor:
    # ... + 2^32 converts int to uint
    color = QColor(QRgba64.fromArgb32(color_int + 2 ** 32))
    return color


def get_int_from_qcolor(color: QColor) -> int:
    # ... - 2^32 converts uint to int
    color_int = color.rgba64().toArgb32() - 2 ** 32
    return color_int
