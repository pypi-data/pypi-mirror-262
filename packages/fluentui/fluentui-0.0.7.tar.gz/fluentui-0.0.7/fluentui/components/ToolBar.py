from typing import Callable

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QToolBar

from .Widget import WidgetMix
from ..gui import Action


class ToolBar(WidgetMix, QToolBar):
    def __init__(self, title='', *,
                 icon_size: int | tuple[int, int] = 16,
                 on_triggered: Callable[[Action], None] = None,
                 **kwargs
                 ):
        super().__init__(title, **kwargs)

        icon_size = (icon_size, icon_size) if isinstance(icon_size, int) else icon_size
        self.setIconSize(QSize(*icon_size))

        if on_triggered: self.actionTriggered.connect(on_triggered)
