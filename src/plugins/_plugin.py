import subprocess
from abc import ABC, abstractmethod
from os import listdir
from os.path import isdir, join, isfile
from typing import Optional

from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLineEdit, QComboBox


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
        return self.set_theme(theme) == theme

    @abstractmethod
    def set_theme(self, theme: str) -> Optional[str]:
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
            for inp in inputs:
                themes = list(self.available_themes.values())
                themes.sort()
                for theme in themes:
                    inp.addItem(theme)

            return inputs

        for theme in ['Light', 'Dark']:
            # provide a line edit, if the possible themes are unknown
            inp = QLineEdit(widget)
            inp.setObjectName(f'inp_{theme}')
            inp.setPlaceholderText(f'{theme} Theme')
            inputs.append(inp)

        return inputs

    def __str__(self):
        return self.name.lower()


class PluginCommandline(Plugin):
    def __init__(self, command: list):
        super().__init__()
        self.command = command

    def set_theme(self, theme: str) -> Optional[str]:
        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        if not (self.available and self.enabled):
            return

        # insert theme in command and run it
        command = self.insert_theme(theme)

        if subprocess.run(command).returncode == 0:
            return theme

    def insert_theme(self, theme: str) -> list:
        command = self.command.copy()
        placeholder = '%t'

        if placeholder not in command:
            for argument in command:
                if placeholder in argument:
                    # replace placeholder with argument, so the theme gets inserted into the argument
                    placeholder = argument
                    break
            assert placeholder != '%t'

        i = command.index(placeholder)
        command.pop(i)
        command.insert(i, placeholder.replace('%t', theme))

        return command

    @property
    def available(self) -> bool:
        # Runs the first entry in the command list with --help
        try:
            return subprocess.run([self.command[0], '--help'], stdout=subprocess.DEVNULL).returncode == 0
        except FileNotFoundError:
            # if no such command is available, the plugin is not available
            return False


class PluginDesktopDependent(Plugin):
    """Plugins that behave differently on different desktops"""

    def __init__(self, strategy_instance: Plugin):
        super().__init__()
        if strategy_instance:
            self._strategy_instance = strategy_instance
        else:
            raise ValueError('Strategy is not valid!')

    @property
    def strategy(self) -> Plugin:
        return self._strategy_instance

    @property
    def available(self) -> bool:
        return self.strategy.available

    def set_theme(self, theme: str) -> Optional[str]:
        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        if not (self.available and self.enabled):
            return

        return self.strategy.set_theme(theme)

    @property
    def available_themes(self) -> dict:
        return self.strategy.available_themes


class ExternalPlugin(Plugin):
    """A class for all plugins whose theme can only be changed externally via communication."""

    def __init__(self, url):
        super().__init__()
        self._url = url

    @property
    def url(self) -> str:
        return ('Please remember to install the plugin.\n'
                f'You can get it here: {self._url}')

    def set_theme(self, theme: str) -> Optional[str]:

        if not (self.available and self.enabled):
            return

        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        # throws error if in debug mode, else ignored
        assert False, 'This is an external plugin, the mode can only be changed externally.'


def inplace_change(filename: str, old_string: str, new_string: str):
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


def get_stuff_in_dir(path: str, type: str) -> [str]:
    """Returns all files or directories in the path
    :param path: The path where to search.
    :param type: The type. Either dir (a directory) or file
    """
    # source: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    # TODO replace with generator
    if type == 'dir':
        return [f for f in listdir(path) if isdir(join(path, f))]
    elif type == 'file':
        return [f for f in listdir(path) if isfile(join(path, f))]
    else:
        raise ValueError('Unknown type! Use dir or file')
