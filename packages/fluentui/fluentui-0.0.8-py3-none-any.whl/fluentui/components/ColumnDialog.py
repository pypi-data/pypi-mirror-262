from .BoxLayout import Column
from .Dialog import Dialog
from .Widget import Widget


class ColumnDialog(Dialog):
    def __init__(self, *,
                 margin='',
                 spacing=0,
                 body: Widget | list[Widget] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs, body=Column(
            margin=margin,
            spacing=spacing,
            items=body,
        ))
