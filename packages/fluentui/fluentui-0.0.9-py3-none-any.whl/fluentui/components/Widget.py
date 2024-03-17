import sys

from PySide6.QtCore import Qt, Signal, QPoint, QObject
from PySide6.QtGui import QKeyEvent, QCloseEvent, QMouseEvent, QFont
from PySide6.QtWidgets import QWidget, QSizePolicy, QLayout, QAbstractScrollArea, QAbstractButton
from typing_extensions import Callable, Iterator, Self

from fluentui.core import Margins
from fluentui.gui import FontMix, Action
from ..core import WA


class WidgetMix:
    on_clicked = Signal(object, object)  # bool, QMouseEvent
    on_key_enter = Signal()
    on_key_esc = Signal()
    on_closed = Signal()

    def __init__(
            self: QWidget | Self, *args,
            parent: 'Widget' = None,
            style='',

            font: FontMix | QFont = None,
            win_title='',
            win_modality: Qt.WindowModality = None,
            win_flags: Qt.WindowType = None,
            menu_policy=Qt.DefaultContextMenu,
            menu_requested: Callable[[QPoint], None] = None,
            attrs: WA | list[WA] = None,
            enabled=True,
            tooltip='',
            cursor: Qt.CursorShape = None,
            mouse_tracking: bool = None,
            margin='0',
            install_event_filter: QObject = None,

            actions: list[Action] = None,
            body: QLayout = None,

            size: int | tuple[int, int] = None,  # 大小
            fixed_size: int | tuple[int, int] = None,  # 固定大小
            width: int = None,  # 固定宽
            height: int = None,  # 固定高
            min_width: int = None,  # 最小宽
            min_height: int = None,  # 最小高
            max_width: int = None,  # 最大宽
            max_height: int = None,  # 最大高

            hor_stretch=0,  # 水平伸缩系数
            ver_stretch=0,  # 垂直伸缩系数
            fill_width=False,  # 填充宽度
            fill_height=False,  # 填充高度
            ignore_width=False,  # 忽略 sizeHint()，视图尽可能获得更多宽度
            ignore_height=False,  # 忽略 sizeHint()，视图尽可能获得更多高度

            grid_row=-1,
            grid_column=0,
            row_span=1,
            column_span=1,
            layout_align=Qt.AlignmentFlag(0),
            layout_dir: Qt.LayoutDirection = None,

            on_clicked: Callable[[bool, QMouseEvent], None] = None,
            on_key_esc: Callable[[], None] = None,
            on_key_enter: Callable[[], None] = None,
            on_closed: Callable[[], None] = None,
            on_destroyed: Callable[[], None] = None,
            **kwargs
    ):
        self.apply_style = style
        self.__is_displayed = False
        self.__is_mouse_pressed = False

        self.grid_row = grid_row
        self.grid_column = grid_column
        self.row_span = row_span
        self.column_span = column_span
        self.layout_align = layout_align

        super().__init__(*args, parent=parent, **kwargs)

        if install_event_filter is not None:
            self.installEventFilter(install_event_filter)

        if on_key_esc: self.on_key_esc.connect(on_key_esc)
        if on_clicked: self.on_clicked.connect(on_clicked)
        if on_key_enter: self.on_key_enter.connect(on_key_enter)
        if on_closed: self.on_closed.connect(on_closed)
        if on_destroyed: self.destroyed.connect(on_destroyed)
        if menu_requested: self.customContextMenuRequested.connect(menu_requested)

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        attrs = attrs or []
        for x in [attrs] if isinstance(attrs, WA) else attrs:
            self.setAttribute(x.attr(), x.on)

        self.setStyleSheet(style)
        self.setWindowTitle(win_title)
        self.setEnabled(enabled)
        self.setToolTip(tooltip)
        self.setContextMenuPolicy(menu_policy)
        self.setContentsMargins(Margins(margin))

        if font: self.setFont(font)
        if win_flags is not None: self.setWindowFlags(win_flags)
        if win_modality is not None: self.setWindowModality(win_modality)
        if cursor is not None:
            view = self.viewport() if isinstance(self, QAbstractScrollArea) else self
            view.setCursor(cursor)

        # 大小策略
        if fill_width or fill_height or ignore_width or ignore_height or hor_stretch > 0 or ver_stretch > 0:
            if (policy := self.sizePolicy()) and fill_width:
                policy.setHorizontalStretch(sys.maxunicode)
                policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
            if fill_height:
                policy.setHorizontalStretch(sys.maxunicode)
                policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
            if ignore_width:
                policy.setHorizontalPolicy(QSizePolicy.Policy.Ignored)
            if ignore_height:
                policy.setVerticalPolicy(QSizePolicy.Policy.Ignored)
            if hor_stretch is not None:
                policy.setHorizontalStretch(hor_stretch)
            if ver_stretch is not None:
                policy.setVerticalStretch(ver_stretch)
            self.setSizePolicy(policy)

        # 设置大小
        if min_width is not None or min_height is not None:
            self.setMinimumSize(min_width or self.minimumWidth(), min_height or self.minimumHeight())
        if max_width is not None or max_height is not None:
            self.setMaximumSize(max_width or self.maximumWidth(), max_height or self.maximumHeight())

        if size is not None:
            size = (size, size) if isinstance(size, int) else size
            self.resize(*size)
        elif fixed_size is not None:
            size = (fixed_size, fixed_size) if isinstance(fixed_size, int) else fixed_size
            self.setFixedSize(*size)
        elif isinstance(width, int) and isinstance(height, int):
            self.setFixedSize(width, height)
        elif isinstance(width, int):
            self.setFixedWidth(width)
        elif isinstance(height, int):
            self.setFixedHeight(height)

        if actions: self.addActions(actions)
        if mouse_tracking is not None: self.setMouseTracking(mouse_tracking)

        if body:
            if layout_dir is not None:
                self.setLayoutDirection(Qt.LayoutDirection(layout_dir))
            self.setLayout(body)

    def keyPressEvent(self: Self, e: QKeyEvent) -> None:
        self.super().keyPressEvent(e)
        key = e.key()
        if key == Qt.Key_Escape:
            self.on_key_esc.emit()
        elif key in (Qt.Key_Enter, Qt.Key_Return):
            self.on_key_enter.emit()

    def closeEvent(self: Self, e: QCloseEvent) -> None:
        self.super().closeEvent(e)
        self.on_closed.emit()

    def mousePressEvent(self: Self, e: QMouseEvent) -> None:
        self.super().mousePressEvent(e)
        self.__is_mouse_pressed = True

    def mouseReleaseEvent(self: Self, e: QMouseEvent):
        self.super().mouseReleaseEvent(e)
        if self.__is_mouse_pressed:
            self.__is_mouse_pressed = False
            args = (self.isChecked(), e) if isinstance(self, QAbstractButton) else (e, False)
            self.on_clicked.emit(*args)

    def addActions(self, actions: list[Action]) -> None:
        for x in actions or []:
            if x.parent() is None:
                x.setParent(self)
        super().addActions(actions)

    def setFont(self: Self, font: QFont | FontMix):
        if isinstance(font, FontMix):
            self.super().setFont(font.merge_to(self.font()))
            return
        self.super().setFont(font)

    def show(self) -> None:
        if not self.__is_displayed:
            if self.apply_style:
                style = f'{style}\n' if (style := self.styleSheet()) else ''
                self.setStyleSheet(style + self.apply_style)
            self.will_display()
        super().show()
        if not self.__is_displayed:
            self.displayed()
            self.__is_displayed = True

    def will_display(self: Self) -> None:
        ...

    def displayed(self) -> None:
        ...

    def super(self) -> Self:
        return super()

    def __iter__(self: Self) -> Iterator['WidgetMix']:
        return iter(self.children())

    def __getitem__(self: Self, index: int) -> 'WidgetMix':
        return self.children()[index]


class Widget(WidgetMix, QWidget):
    ...
