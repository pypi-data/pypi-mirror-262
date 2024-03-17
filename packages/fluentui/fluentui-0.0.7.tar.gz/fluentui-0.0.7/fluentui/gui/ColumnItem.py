class ColumnItem:
    def __init__(self, value: object, alias='', visible=False):
        self.value = value
        self.alias = alias
        self.visible = visible

    def __repr__(self) -> str:
        return f'{self.value}'
