from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QAbstractButton

from .Widget import WidgetMix


class AbstractButtonMix(WidgetMix):
    def __init__(self: QAbstractButton,
                 text: str = '', *,
                 tool_tip: str = '',
                 icon: QIcon | str = None,
                 icon_size: int | tuple[int, int] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        if text:
            self.setText(text)

        if icon:
            self.setIcon(icon if isinstance(icon, QIcon) else QIcon(icon))

        if icon_size is not None:
            flag = isinstance(icon_size, tuple)
            size = QSize(*icon_size) if flag else QSize(icon_size, icon_size)
            self.setIconSize(size)

        self.setToolTip(tool_tip)


class AbstractButton(AbstractButtonMix, QAbstractButton):
    ...
