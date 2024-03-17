from PySide6.QtCore import QSize


class Size(QSize):
    def __init__(self, *size: int | tuple[int, int] | QSize):
        if size and isinstance(size, tuple):
            size = (size[0], size[1])
        super().__init__(*size)
