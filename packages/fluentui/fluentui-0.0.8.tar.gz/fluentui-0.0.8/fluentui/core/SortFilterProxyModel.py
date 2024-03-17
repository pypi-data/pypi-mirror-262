from PySide6.QtCore import QObject, QSortFilterProxyModel

from .AbsItemModel import AbsItemModel
from .AbsProxyModel import AbsProxyModelMix


class SortFilterProxyModelMix(AbsProxyModelMix):
    def __init__(self, source: AbsItemModel = None, parent: QObject = None):
        super().__init__(parent)
        if source is not None:
            self.setSourceModel(source)


class SortFilterProxyModel(SortFilterProxyModelMix, QSortFilterProxyModel):
    ...
