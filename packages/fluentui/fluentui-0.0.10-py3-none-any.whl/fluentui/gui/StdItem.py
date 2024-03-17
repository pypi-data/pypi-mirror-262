from __future__ import annotations

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QStandardItem, QGradient, QColor, QBrush

from fluentui.gui import FontMix


class StdItem(QStandardItem):
    def __init__(self, text=None,
                 children: list['StdItem'] = None, *,
                 rows: int = None,
                 columns=1,
                 text_align: Qt.AlignmentFlag = None,
                 flags: Qt.ItemFlags = None,
                 background: QBrush | QColor | Qt.GlobalColor | QGradient = None,
                 foreground: QBrush | QColor | Qt.GlobalColor | QGradient = None,
                 size_hint: int = None,
                 font: FontMix = None,
                 ):
        if rows is not None:
            super().__init__(rows, columns=columns)
        else:
            super().__init__()

        if background and isinstance(background, str):
            background = QColor(background)
        if foreground and isinstance(foreground, str):
            foreground = QColor(foreground)

        if flags is not None: self.setFlags(flags)
        if text: self.setData(text, Qt.DisplayRole)
        if text_align is not None: self.setTextAlignment(text_align)
        if background is not None: self.setBackground(background)
        if foreground is not None: self.setForeground(foreground)
        if size_hint is not None: self.setSizeHint(QSize(0, size_hint))
        if font is not None: self.setFont(font.merge_to(self.font()))

        for x in children or []:
            self.appendRow(x)

    def setTextAlignment(self, align: Qt.AlignmentFlag) -> None:
        super().setTextAlignment(Qt.AlignmentFlag(align))
