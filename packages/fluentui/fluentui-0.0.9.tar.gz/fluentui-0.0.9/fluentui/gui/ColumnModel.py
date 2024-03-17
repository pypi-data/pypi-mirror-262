from PySide6.QtCore import QAbstractTableModel, QObject, QModelIndex, Qt, QPersistentModelIndex
from polars import DataFrame

from .ColumnField import ColumnField
from ..core.AbsItemModel import AbsItemModelMix
from ..namespce import ItemDataRole, Alignment


class ColumnModel(AbsItemModelMix, QAbstractTableModel):
    def __init__(self,
                 parent: QObject = None, *,
                 table: list[ColumnField] = None,
                 data: list[dict[str, object]] = None
                 ):
        super().__init__(parent)

        self.table = table or []
        self.fields = [x.title for x in self.table]
        self.columns = {x: i for i, x in enumerate(self.fields)}

        self.df = DataFrame(schema={x.title: x.origin_type() for x in self.table})
        if data is not None:
            self.append(data)

    def rowCount(self, parent=QModelIndex()) -> int:
        """ 行数 """
        return self.df.height

    def columnCount(self, parent=QModelIndex()) -> int:
        """ 列数 """
        return self.df.width

    def headerData(self, section: int, orientation=Qt.Orientation.Horizontal, role=ItemDataRole.Display) -> object:
        """ 头数据 """
        if role == ItemDataRole.Display:
            if orientation == Qt.Orientation.Horizontal and self.table:
                return self.table[section].alias
        elif role == ItemDataRole.TextAlignment:
            if orientation == Qt.Orientation.Horizontal:
                return Alignment.Left | Alignment.VCenter
        return super().headerData(section, orientation, role)

    def removeRows(self, row: int, count: int, parent=QModelIndex()) -> None:
        """ 移除行 """
        self.beginRemoveRows(parent, row, row + count - 1)
        self.df = self.df[:row].extend(self.df[row + count:])
        self.endRemoveRows()
        return True

    def data(self, index: QModelIndex, role=ItemDataRole.Display) -> object:
        """ 项目数据 """
        if role in (ItemDataRole.Display, ItemDataRole.Edit):
            return self.df[index.row(), index.column()]
        return None

    def setData(self, index: QModelIndex, value: object, role=ItemDataRole.Edit) -> bool:
        """ 设置数据 """
        if role in (ItemDataRole.Display, ItemDataRole.Edit):
            self.df[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def append(self, data: dict | list[dict] = None, row=-1, reserve_blank_row=False, remove_rows=False) -> None:
        """ 添加行 """
        if remove_rows:
            self.removeRows(0, self.rowCount())

        reserve_blank_row = reserve_blank_row or data is None
        data = data or []
        data = data if isinstance(data, list) else [data]

        if reserve_blank_row:  # 追加空行
            if not data:
                type_dict = self.df.item(0, 0).__class__.__annotations__
            else:
                type_dict = {k: type(v) for k, v in data[0].items()}
            data.append({k: v() for k, v in type_dict.items()})

        first = row if row >= 0 else self.rowCount()
        last = first + len(data) - 1

        fields = {x.title: None for x in self.table}
        data = [fields | x for x in data]

        self.beginInsertRows(QModelIndex(), first, last)
        self._append_df(row, data, first)
        self.endInsertRows()

    def update_data(self, row: int | QModelIndex, data: dict, roles: list = None):
        row = row if isinstance(row, int) else row.row()
        roles = roles or [ItemDataRole.Display]

        for column, name in enumerate(self.fields):
            if name not in data:
                continue
            index = self.index(row, column)
            self.df[row, column] = data[name]
            self.dataChanged.emit(index, index, roles)

    def _append_df(self, row: int, data: list[dict[str, object]], first: int) -> None:
        df = DataFrame(
            {key: value for key, value in x.items()}
            for x in data
        )
        if row == -1:
            setattr(self, 'df', df) if self.df.is_empty() else self.df.extend(df)
        else:
            self.df = self.df[:first].extend([df, self.df[first:]])

    def __getattr__(self, index: int | QModelIndex | QPersistentModelIndex) -> dict[str, object]:
        row = index if isinstance(index, int) else index.row()
        return self.df.row(row, named=True)
