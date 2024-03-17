from enum import Flag, IntEnum, IntFlag, Enum

from PySide6.QtCore import Qt


class Alignment(IntFlag):
    Top = Qt.AlignmentFlag.AlignTop
    Right = Qt.AlignmentFlag.AlignRight
    Left = Qt.AlignmentFlag.AlignLeft

    Center = Qt.AlignmentFlag.AlignCenter
    HCenter = Qt.AlignmentFlag.AlignHCenter
    VCenter = Qt.AlignmentFlag.AlignVCenter


class ItemDataRole(IntEnum):
    Display = 0
    Decoration = 1
    Edit = 2
    ToolTip = 3
    StatusTip = 4
    WhatsThis = 5
    SizeHint = 13

    Font = 6
    TextAlignment = 7
    Background = 8
    Foreground = 9
    CheckState = 10
    InitialSortOrder = 14

    AccessibleText = 11
    AccessibleDescription = 12

    User = 256


class Orientation(Flag):
    Horizontal = 0x1
    Vertical = 0x1


class ScrollBarPolicy(Enum):
    AsNeeded = 0x0
    AlwaysOff = 0x1
    AlwaysOn = 0x2
