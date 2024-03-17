from PySide6.QtGui import QFont, QFontDatabase


class FontMix:
    def __init__(self, *,
                 src: list[str] = None,
                 point_size=0,
                 pixel_size=0,
                 weight=QFont.Weight.Normal,
                 families='Microsoft YaHei UI'
                 ):
        self.src = src
        self.weight = weight
        self.point_size = point_size
        self.pixel_size = pixel_size
        self.families = [x.strip(' ') for x in families.split(',')]

    def merge_to(self, font: QFont) -> QFont:
        for x in self.src or []:
            _id = QFontDatabase.addApplicationFont(x)
            QFontDatabase.applicationFontFamilies(_id)

        font.setWeight(self.weight)
        font.setFamilies(self.families)

        if self.point_size > 0:
            font.setPointSize(self.point_size)
        if self.pixel_size > 0:
            font.setPixelSize(self.pixel_size)

        return font
