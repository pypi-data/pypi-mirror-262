from PySide6.QtWidgets import QListView

from .AbsItemView import AbsItemViewMix
from ..gui import StdModel


class ListView(AbsItemViewMix, QListView):
    def __init__(self, *, uniform_item_sizes=False, spacing=0, **kwargs):
        super().__init__(**kwargs)
        self.setSpacing(spacing)
        self.setUniformItemSizes(uniform_item_sizes)

    def model(self) -> StdModel:
        return super().model()
