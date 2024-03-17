from PySide6.QtWidgets import QSpinBox

from .AbstractSpinBoxMix import AbstractSpinBoxMix


class SpinBoxMix(AbstractSpinBoxMix):
    def __init__(self: QSpinBox, value=0, *,
                 minimum=0,
                 maximum=99,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setValue(value)


class SpinBox(SpinBoxMix, QSpinBox):
    ...
