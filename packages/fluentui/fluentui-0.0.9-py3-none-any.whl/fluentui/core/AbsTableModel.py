from PySide6.QtCore import QAbstractTableModel

from .AbsItemModel import AbsItemModelMix


class AbsTableModel(AbsItemModelMix, QAbstractTableModel):
    ...
