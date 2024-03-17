from .BoxLayout import Row
from .Widget import Widget


class RowWidget(Widget):
    def __init__(self, *,
                 margin='0',
                 spacing=0,
                 body: Widget | list[Widget] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs, body=Row(
            margin=margin,
            spacing=spacing,
            items=body,
        ))
