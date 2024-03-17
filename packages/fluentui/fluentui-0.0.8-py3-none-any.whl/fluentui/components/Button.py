from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QCheckBox, QAbstractButton, QRadioButton
from typing_extensions import Self, Callable, Union

from .Widget import WidgetMix


class AbsButtonMix(WidgetMix):
    Self = Union[QAbstractButton, Self]

    def __init__(self: Self,
                 text: str = '', *,
                 icon: QIcon | str = None,
                 icon_size: int | tuple[int, int] = 16,
                 checked=False,
                 checkable: bool = None,
                 auto_exclusive: bool = None,
                 on_toggled: Callable[[bool], None] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        if on_toggled: self.toggled.connect(on_toggled)

        self.setText(text)
        self.setIconSize(icon_size)
        if auto_exclusive is not None:
            self.setAutoExclusive(auto_exclusive)
        if checkable is not None:
            self.setCheckable(checkable)
        self.setChecked(checked)
        if icon: self.setIcon(icon)

    def setIcon(self: Self, icon: QIcon | str) -> None:
        icon = QIcon(icon) if isinstance(icon, str) else icon
        self.super().setIcon(icon)

    def setIconSize(self, size: int | tuple[int, int]):
        size = size if isinstance(size, tuple) else (size, size)
        super().setIconSize(QSize(*size))


class Button(AbsButtonMix, QPushButton):
    def __init__(self, text='', *,
                 default: bool = None,
                 auto_default: bool = None,
                 **kwargs
                 ):
        super().__init__(text, **kwargs)
        if default is not None:
            self.setDefault(default)
        if auto_default is not None:
            self.setAutoDefault(auto_default)

    def setIcon(self, icon: str | QIcon) -> None:
        icon = QIcon(icon) if isinstance(icon, str) else icon
        super().setIcon(icon)


class SubtleButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(text, **kwargs)
        self.setStyleSheet(
            'SubtleButton {\n'
            '    background: transparent;\n'
            '    border: none;\n'
            '    padding: 5\n'
            '}\n'
            ':hover { background: #f5f5f5 }\n'
            ':pressed { background: #e0e0e0 }'
        )


class CheckBox(AbsButtonMix, QCheckBox):
    ...


class RadioButton(AbsButtonMix, QRadioButton):
    def __init__(self, text: str, **kwargs):
        super().__init__(text, **kwargs)
