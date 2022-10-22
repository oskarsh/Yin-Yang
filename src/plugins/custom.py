import re

from PySide6.QtWidgets import QLineEdit

from src.plugins._plugin import PluginCommandline


class Custom(PluginCommandline):
    def __init__(self):
        super().__init__([])

    def insert_theme(self, theme: str) -> list:
        # splits at every non-escaped space
        # src: https://stackoverflow.com/questions/18092354/python-split-string-without-splitting-escaped-character
        command = re.split(r'(?<!\\) ', theme)
        return command

    @property
    def available(self) -> bool:
        return True

    def get_input(self, widget):
        inputs: list[QLineEdit | QLineEdit] = super().get_input(widget)
        inputs[0].setPlaceholderText('Light script')
        inputs[1].setPlaceholderText('Dark script')
        return inputs
