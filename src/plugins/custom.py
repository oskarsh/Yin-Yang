from PySide6.QtWidgets import QLineEdit

from src.plugins._plugin import PluginCommandline


class Custom(PluginCommandline):
    def __init__(self):
        super().__init__(['{theme}'])

    @property
    def available(self) -> bool:
        return True

    def get_input(self, widget):
        inputs: list[QLineEdit | QLineEdit] = super().get_input(widget)
        inputs[0].setPlaceholderText('Light script')
        inputs[1].setPlaceholderText('Dark script')
        return inputs
