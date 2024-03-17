from .BoxLayout import Column
from .Widget import Widget


class ColumnWidget(Widget):
    def __init__(self, *,
                 margin='0',
                 spacing=0,
                 body: Widget | list[Widget] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs, body=Column(
            margin=margin,
            spacing=spacing,
            items=body,
        ))
