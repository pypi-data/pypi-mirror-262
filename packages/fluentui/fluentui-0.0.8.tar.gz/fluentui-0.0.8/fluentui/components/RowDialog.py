from .BoxLayout import Row
from .Dialog import Dialog
from .Widget import Widget


class RowDialog(Dialog):
    def __init__(self, *,
                 margin='',
                 spacing=0,
                 body: Widget | list[Widget] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs, body=Row(
            margin=margin,
            spacing=spacing,
            items=body,
        ))
