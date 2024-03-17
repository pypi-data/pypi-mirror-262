from PySide6.QtCore import QObject, QModelIndex
from PySide6.QtGui import QColor, QPainter, Qt, QPalette
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle
from typing_extensions import TYPE_CHECKING

from .AbsItemDelegate import AbsItemDelegateMix

if TYPE_CHECKING:
    from .TableView import TableView
from ..namespce import ItemDataRole


class StyledItemDelegate(AbsItemDelegateMix, QStyledItemDelegate):
    ...


class ItemViewDelegate(StyledItemDelegate):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.high_bgcolor = QColor('#cde8ff')  # 高亮背景颜色
        self.line_color = QColor('#ccd0da')  # 线颜色

    def paint(self, painter: QPainter, opt: QStyleOptionViewItem, index: QModelIndex) -> None:
        bgcolor = index.data(ItemDataRole.Background) or self.high_bgcolor
        fgcolor = index.data(ItemDataRole.Foreground) or Qt.GlobalColor.black

        p = opt.palette
        p.setColor(QPalette.ColorRole.Highlight, bgcolor)
        p.setColor(QPalette.ColorRole.HighlightedText, fgcolor)

        if opt.state & QStyle.StateFlag.State_HasFocus:
            opt.state ^= QStyle.StateFlag.State_HasFocus
            # super().paint(painter, opt, index)
            # rect = opt.rect.adjusted(1, 1, -1, -1)
            # painter.setPen(QPen(QColor('#008000'), 2, Qt.PenStyle.DotLine))
            # painter.drawRect(rect)
            # return

        super().paint(painter, opt, index)


class TableViewDelegate(ItemViewDelegate):
    def paint(self, painter: QPainter, opt: QStyleOptionViewItem, index: QModelIndex) -> None:
        super().paint(painter, opt, index)
        painter.setPen(self.line_color)
        painter.drawLine(opt.rect.bottomLeft(), opt.rect.bottomRight())

    def parent(self) -> 'TableView':
        return super().parent()
