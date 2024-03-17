from PySide6.QtWidgets import QToolButton

from .AbstractButton import AbstractButtonMix


class ToolButton(AbstractButtonMix, QToolButton):
    def __init__(self, text='', **kwargs):
        super().__init__(text, **kwargs)
