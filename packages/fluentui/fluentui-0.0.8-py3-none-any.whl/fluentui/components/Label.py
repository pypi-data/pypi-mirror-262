from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QSizePolicy

from .Widget import WidgetMix
from ..namespce import Alignment


class Label(WidgetMix, QLabel):
    def __init__(self, text='', align: Qt.AlignmentFlag = None, **kwargs):
        super().__init__(text, **kwargs)
        if 'fill_width' not in kwargs and 'ignore_width' not in kwargs:
            self.setSizePolicy(QSizePolicy.Policy.Fixed, self.sizePolicy().verticalPolicy())
        if align is not None:
            self.setAlignment(align)

    def setAlignment(self, align: Alignment) -> None:
        super().setAlignment(Qt.AlignmentFlag(align))
