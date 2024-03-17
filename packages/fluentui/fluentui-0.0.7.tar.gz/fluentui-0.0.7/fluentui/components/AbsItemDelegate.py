from PySide6.QtCore import QModelIndex, QSize, QLocale
from PySide6.QtWidgets import QStyleOptionViewItem, QWidget, QAbstractItemDelegate
from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from .AbsItemView import AbsItemView
from ..core import AbsItemModel


class AbsItemDelegateMix:
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        """ 创建编辑器 """
        return self.parent().createEditor(parent, option, index)

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        """ 更新编辑器 """
        self.parent().updateEditorGeometry(editor, option, index)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        """ 设置编辑器数据 """
        self.parent().setEditorData(editor, index)

    def setModelData(self, editor: QWidget, model: AbsItemModel, index: QModelIndex) -> None:
        """ 设置模型数据 """
        self.parent().setModelData(editor, model, index)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        """ 项目大小提示 """
        return self.parent().itemSizeHint(option, index)

    def displayText(self, value: object, locale: QLocale) -> str:
        """ 项目文本 """
        return self.parent().displayText(value, locale)

    def parent(self) -> 'AbsItemView':
        return super().parent()

    def super(self) -> QAbstractItemDelegate:
        return super()


class AbsItemDelegate(AbsItemDelegateMix, QAbstractItemDelegate):
    ...

