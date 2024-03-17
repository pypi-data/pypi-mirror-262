from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit

from fluentui.components.ScrollArea import ScrollAreaMix


class TextEditMix(ScrollAreaMix):
    def __init__(self: QTextEdit,
                 text='', *,
                 read_only=False,
                 undo_redo_enabled=True,
                 document_margin=0,
                 accept_rich_text=True,
                 on_text_change: Callable[[], None] = None,
                 alignment: Qt.AlignmentFlag = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        if on_text_change: self.textChanged.connect(on_text_change)

        self.setText(text)
        self.setReadOnly(read_only)
        self.setAcceptRichText(accept_rich_text)
        self.setUndoRedoEnabled(undo_redo_enabled)
        self.document().setDocumentMargin(document_margin)
        if alignment is not None: self.setAlignment(alignment)

    def adjustFixedHeight(self: QTextEdit, width=0) -> None:
        if (d := self.document()) and width > 0:
            d.setTextWidth(width)
            d.setTextWidth(idea_width := int(d.idealWidth()))
            self.setFixedSize(idea_width, d.size().toSize().height())
        else:
            d.setTextWidth(d.idealWidth())
            self.setFixedHeight(d.size().toSize().height())


class TextEdit(TextEditMix, QTextEdit):
    ...
