from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from typing_extensions import Callable


class ColumnField(FieldInfo):
    def __init__(self, default=PydanticUndefined, *,
                 default_factory: Callable[[], object] = None,
                 title='',
                 alias='',
                 visible=False,
                 annotation: type = None):
        self.visible = visible
        super().__init__(
            default=default,
            default_factory=default_factory,
            title=title,
            alias=alias,
            annotation=annotation
        )

    def __set_name__(self, owner, name):
        self.title = name

    def origin_type(self) -> type:
        annotation = self.annotation
        return getattr(annotation, '__origin__', annotation)
