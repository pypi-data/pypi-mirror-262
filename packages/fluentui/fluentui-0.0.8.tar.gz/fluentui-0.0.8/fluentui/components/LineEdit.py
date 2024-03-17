from typing import Callable

from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QLineEdit

from .Widget import WidgetMix


class LineEdit(WidgetMix, QLineEdit):
    def __init__(self, text: object = '', *,
                 placeholder='',
                 read_only=False,
                 text_changed: Callable[[str], ...] = None,
                 validator: QValidator = None,
                 **kwargs
                 ):
        super().__init__(f'{text}', **kwargs)
        self.setReadOnly(read_only)
        self.setPlaceholderText(placeholder)

        if validator is not None:
            self.setValidator(validator)

        if text_changed:
            self.textChanged.connect(text_changed)

    def setText(self, text: object, block_signals=False):
        super().setText(f'{text}')
        if block_signals: self.blockSignals(True)
        self.setCursorPosition(0)
        if block_signals: self.blockSignals(False)

    def to_int(self) -> int:
        return int(self.to_float())

    def to_float(self) -> float:
        return float(self.text() or 0)
