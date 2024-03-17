from PySide6.QtCore import QAbstractProxyModel

from .AbsItemModel import AbsItemModelMix


class AbsProxyModelMix(AbsItemModelMix):
    ...


class AbsProxyModel(AbsProxyModelMix, QAbstractProxyModel):
    ...
