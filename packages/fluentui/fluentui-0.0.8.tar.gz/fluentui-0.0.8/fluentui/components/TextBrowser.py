from PySide6.QtWidgets import QTextBrowser
from typing_extensions import Callable

from fluentui.components.TextEdit import TextEditMix


class TextBrowser(TextEditMix, QTextBrowser):
    def __init__(self, text='', *,
                 open_links=True,
                 open_external_links=False,
                 on_anchor_clicked: Callable[[str], None] = None,
                 **kwargs
                 ):
        super().__init__(text, **kwargs)
        if on_anchor_clicked: self.anchorClicked.connect(on_anchor_clicked)

        self.setOpenLinks(open_links)
        self.setOpenExternalLinks(open_external_links)
