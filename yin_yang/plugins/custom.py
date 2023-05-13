import subprocess

from PySide6.QtWidgets import QLineEdit

from ._plugin import PluginCommandline


class Custom(PluginCommandline):
    def __init__(self):
        super().__init__([])

    def insert_theme(self, theme: str) -> list:
        return [theme]

    @property
    def available(self) -> bool:
        return True

    def get_input(self, widget):
        inputs: list[QLineEdit | QLineEdit] = super().get_input(widget)
        inputs[0].setPlaceholderText('Light script')
        inputs[1].setPlaceholderText('Dark script')
        return inputs

    def set_theme(self, theme: str):
        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        if not (self.available and self.enabled):
            return

        # insert theme in command and run it
        command = self.insert_theme(theme)
        # set shell=True to avoid having to separate between arguments
        subprocess.check_call(command, shell=True)
