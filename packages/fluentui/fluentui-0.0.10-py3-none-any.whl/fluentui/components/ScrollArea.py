from PySide6.QtWidgets import QScrollArea

from .AbsScrollArea import AbsScrollAreaMix


class ScrollAreaMix(AbsScrollAreaMix):
    ...


class ScrollArea(ScrollAreaMix, QScrollArea):
    ...
