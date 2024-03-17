from enum import Enum
from typing import Self

from PySide6.QtCore import Qt


class WA(Enum):
    DeleteOnClose = 55  # 接受关闭事件时删除小部件
    StyledBackground = 93  # 小部件使用 style 绘制背景
    # 小部件具有半透明背景，即小部件的任何非不透明区域都将是半透明的，因为小部件将具有 Alpha 通道。
    # 跨平台不统一支持在小部件显示后切换此属性。
    TranslucentBackground = 120

    def __init__(self, _, on=True):
        self.on = on

    def off(self) -> Self:
        self.on = False
        return self

    def attr(self) -> Qt.WidgetAttribute:
        return Qt.WidgetAttribute(self.value)
