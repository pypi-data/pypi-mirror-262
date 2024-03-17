from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QAbstractScrollArea

from .Frame import FrameMix
from ..namespce import ScrollBarPolicy


class AbsScrollAreaMix(FrameMix):
    def __init__(self: QScrollArea,
                 hor_scroll_bar_policy: ScrollBarPolicy = None,
                 ver_scroll_bar_policy: ScrollBarPolicy = None,
                 **kwargs):
        super().__init__(**kwargs)
        if hor_scroll_bar_policy is not None:
            self.setHorizontalScrollBarPolicy(hor_scroll_bar_policy)
        if ver_scroll_bar_policy is not None:
            self.setVerticalScrollBarPolicy(ver_scroll_bar_policy)

    def setHorizontalScrollBarPolicy(self, policy: ScrollBarPolicy):
        super().setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(policy.value))

    def setVerticalScrollBarPolicy(self, policy: ScrollBarPolicy):
        super().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy(policy.value))


class AbsScrollArea(AbsScrollAreaMix, QAbstractScrollArea):
    ...
