import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget
from typing_extensions import Callable, Never, Union

from .. import FluentuiLightStyle
from ..gui import FontMix


class App(QApplication):
    def __init__(self, font: FontMix | QFont = None,
                 show: Callable[[], QWidget] = None,
                 quit_on_last_window_closed=True,
                 about_to_quit: Callable[[], None] = None,
                 ):

        self.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        self.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        super().__init__(sys.argv)

        if about_to_quit:
            self.aboutToQuit.connect(about_to_quit)

        if font:
            self.setFont(font)

        self.setStyleSheet(FluentuiLightStyle)
        self.setQuitOnLastWindowClosed(quit_on_last_window_closed)

        if widget := show and show():
            widget.show()
            self.exec()

    def exec(self) -> Never:
        return sys.exit(super().exec())

    def setFont(self, font: Union[QFont, FontMix]):
        if isinstance(font, FontMix):
            super().setFont(font.merge_to(self.font()))
            return
        super().setFont(font)
