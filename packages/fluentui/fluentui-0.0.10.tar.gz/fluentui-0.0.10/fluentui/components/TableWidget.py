from PySide6.QtWidgets import QTableWidget

from fluentui.components.TableView import TableViewMix


class TableWidget(TableViewMix, QTableWidget):
    def __init__(self, rows=0, columns=0, **kwargs):
        super().__init__(**kwargs)
        self.setRowCount(rows)
        self.setColumnCount(columns)
