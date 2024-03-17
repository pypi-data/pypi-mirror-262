from typing import Callable

from PySide6.QtWidgets import QDialog

from .Widget import WidgetMix


class Dialog(WidgetMix, QDialog):
    def __init__(self, *,
                 on_accepted: Callable[[], None] = None,
                 on_rejected: Callable[[], None] = None,
                 on_finished: Callable[[int], None] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        if on_accepted: self.accepted.connect(on_accepted)
        if on_rejected: self.rejected.connect(on_rejected)
        if on_finished: self.finished.connect(on_finished)
