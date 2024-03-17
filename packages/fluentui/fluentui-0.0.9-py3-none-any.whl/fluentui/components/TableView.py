from PySide6.QtCore import QPoint, QModelIndex
from PySide6.QtWidgets import QTableView, QWidget

from .AbsItemView import AbsItemViewMix, Self
from .StyledItemDelegate import TableViewDelegate


class TableViewMix(AbsItemViewMix):
    def __init__(self: QTableView | Self, *args,
                 default_row_height=24,  # 默认行高
                 default_col_width: int = None,  # 默认列宽
                 min_row: int = None,  # 最小行高
                 max_row: int = None,  # 最大行高
                 min_col: int = None,  # 最小列宽
                 max_col: int = None,  # 最大列宽
                 word_wrap=True,
                 auto_scroll=False,
                 hor_header_visible=True,
                 ver_header_visible=True,
                 stretch_last_section=False,
                 **kwargs
                 ):
        super().__init__(*args, **kwargs)
        hor_header = self.horizontalHeader()
        ver_header = self.verticalHeader()

        if default_col_width:
            hor_header.setDefaultSectionSize(default_col_width)  # 默认列宽
        if min_col: hor_header.setMinimumSectionSize(min_col)  # 最小列宽
        if max_col: hor_header.setMaximumSectionSize(max_col)  # 最大列宽
        hor_header.setVisible(hor_header_visible)

        ver_header.setDefaultSectionSize(default_row_height)  # 默认行高
        if min_row: ver_header.setMinimumSectionSize(min_row)  # 最小行高
        if max_row: ver_header.setMaximumSectionSize(max_row)  # 最大行高
        ver_header.setVisible(ver_header_visible)

        self.setShowGrid(False)
        self.setWordWrap(word_wrap)
        self.setAutoScroll(auto_scroll)
        self.horizontalHeader().setStretchLastSection(stretch_last_section)


class TableView(TableViewMix, QTableView):
    def __init__(self, **kwargs):
        kwargs.setdefault('delegate', TableViewDelegate())
        super().__init__(**kwargs)

    def indexAt(self, pos: QPoint | QWidget) -> QModelIndex:
        if isinstance(pos, QWidget):
            pos = pos.mapToGlobal(pos.pos())
            return self.indexAt(self.mapFromGlobal(pos))
        return super().indexAt(pos)

    # def mouseMoveEvent(self, e: QMouseEvent):
    #     index = self.indexAt(e.position().toPoint())
    #     if self.hovered_row != index.row():
    #         self._update_hovered_row_color(self.hovered_row)
    #         self.hovered_row = index.row()
    #         self._update_hovered_row_color(self.hovered_row)
    #     super().mouseMoveEvent(e)
    #
    # def _update_hovered_row_color(self, row: int):
    #     if not (m := self.model()):
    #         return
    #     for col in range(m.columnCount()):
    #         self.update(m.index(row, col))
