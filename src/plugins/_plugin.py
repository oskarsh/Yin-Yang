from abc import ABC, abstractmethod
from os import listdir
from os.path import isdir, join, isfile

from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLineEdit, QComboBox


class Plugin(ABC):
    """An abstract base class for plugins"""

    # default themes
    theme_dark = None
    theme_bright = None

    def __init__(self, theme_dark: str = '', theme_bright: str = ''):
        # check default values
        assert self.theme_dark is not None or self.theme_bright is not None,\
            'Light and / or dark theme have no default value!'

        # set the themes
        if theme_dark.isprintable() and theme_dark != self.theme_dark:
            self.theme_dark = theme_dark
        if theme_bright.isprintable() and theme_bright != self.theme_bright:
            self.theme_bright = theme_bright

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
    def available_themes(self) -> dict[str, str]:
        """Return a list of available themes
        :return: Dict[intern_name, readable_name]
        """
        return {}

    def set_mode(self, dark: bool):
        """Set the dark or light theme"""

        theme = self.theme_dark if dark else self.theme_bright
        self.set_theme(theme)

    @abstractmethod
    def set_theme(self, theme: str):
        """Sets a specific theme"""
        raise NotImplementedError

    def get_widget(self, area) -> QGroupBox:
        """Returns a widget for the settings menu
        area: scrollAreaWidgetContents
        """

        widget = QGroupBox(area)
        widget.setCheckable(True)
        widget.setTitle(self.name)
        widget.setObjectName('group' + self.name)

        horizontal_layout = QHBoxLayout(widget)

        for inp in self.__get_input(widget):
            horizontal_layout.addWidget(inp)

        return widget

    def __get_input(self, widget):
        """Returns two inputs for dark and light theme for the config gui"""
        inputs = []

        if self.available_themes != {}:
            # use a combobox if the possible themes are known
            inputs = [QComboBox(widget), QComboBox(widget)]

            # add all theme names
            for inp in inputs:
                for theme in self.available_themes.values():
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

    def __str__(self):
        return self.name


class PluginDesktopDependent(Plugin):
    """Plugins that behave differently on different desktops"""

    @abstractmethod
    def __init__(self, desktop: str):
        super().__init__()

    @property
    @abstractmethod
    def strategy(self) -> Plugin:
        raise NotImplementedError

    @property
    def available(self) -> bool:
        return self.strategy.available

    @property
    def theme_dark(self):
        if hasattr(self, 'strategy'):
            # needed since the plugin class checks if the themes are set correctly
            # in it's init
            return self.strategy.theme_dark
        else:
            return ''

    @theme_dark.setter
    def theme_dark(self, theme: str):
        self.strategy.theme_dark = theme

    @property
    def theme_bright(self):
        if hasattr(self, 'strategy'):
            return self.strategy.theme_bright
        else:
            return ''

    @theme_bright.setter
    def theme_bright(self, theme: str):
        self.strategy.theme_bright = theme

    def set_theme(self, theme: str):
        self.strategy.set_theme(theme)

    @property
    def available_themes(self) -> dict[str, str]:
        return self.strategy.available_themes


def inplace_change(filename, old_string, new_string):
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
    if type == 'dir':
        return [f for f in listdir(path) if isdir(join(path, f))]
    elif type == 'file':
        return [f for f in listdir(path) if isfile(join(path, f))]
    else:
        raise ValueError('Unknown type! Use dir or file')
