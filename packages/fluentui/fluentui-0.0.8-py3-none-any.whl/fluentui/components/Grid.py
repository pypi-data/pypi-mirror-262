from PySide6.QtWidgets import QGridLayout

from .Widget import WidgetMix
from ..core import Margins


class Grid(QGridLayout):
    def __init__(self, *, margins='', items: list['WidgetMix'] = None):
        super().__init__()
        if margins: self.setContentsMargins(Margins(margins))
        for x in items or []:
            self.addWidget(x)

    def addWidget(self, item: WidgetMix) -> None:
        row = item.row if item.row >= 0 else self.rowCount()
        super().addWidget(item, row, item.column, item.rowSpan, item.columnSpan, item.align)

    def rowCount(self) -> int:
        return super().rowCount() if self.itemAt(0) else 0

    def columnCount(self) -> int:
        return super().columnCount() if self.itemAt(0) else 0
