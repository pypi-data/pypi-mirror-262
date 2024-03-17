from PySide6.QtWidgets import QWidget


class Qss:
    def __init__(self,
                 color='',  # 前景颜色
                 bgcolor='',  # 背景颜色
                 alternate_bgcolor='',  # 交替颜色 QListView, QTableView, QTreeView
                 top='', right='', bottom='', left='',  # QTabBar, QTabWidget
                 padding='', padding_top='', padding_right='', padding_bottom='', padding_left='',  # box-model
                 margin='', margin_top='', margin_right='', margin_bottom='', margin_left='',  # box-model
                 border='', border_top='', border_right='', border_bottom='', border_left='',  # box-model
                 spacing='',  # 间距 QToolBar
                 # 伪状态 | 子控件
                 hover: 'Qss' = None,
                 pressed: 'Qss' = None,
                 ):
        self.style_dict = {
            'color': color,
            'background-color': bgcolor,
            'alternate-background-color': alternate_bgcolor,
            'top': top,
            'right': right,
            'bottom': bottom,
            'left': left,
            'padding': padding,
            'padding-top': padding_top,
            'padding-left': padding_left,
            'padding-bottom': padding_bottom,
            'padding-right': padding_right,
            'margin': margin,
            'margin-top': margin_top,
            'margin-left': margin_left,
            'margin-bottom': margin_bottom,
            'margin-right': margin_right,
            'border': border,
            'border-top': border_top,
            'border-bottom': border_bottom,
            'border-left': border_left,
            'border-right': border_right,
            'spacing': spacing,
        }

        self.style_list = {
            ':hover': hover,
            ':pressed': pressed,
        }

    def apply(self, view: QWidget) -> str:
        wid = id(self)
        if not view.property('id'):
            view.setProperty('id', wid)

        s = f'[id="{wid}"] {{\n'
        for k, v in self.style_dict.items():
            if not v:
                continue
            s += f"    {k}: {v};\n"

        if not s.endswith(';\n'):
            return ''

        s += "}"
        for key, value in self.style_list.items():
            if value is None:
                continue
            s += f'\n{key}'
            s += value.sub_style()

        view.setStyleSheet(s)
        return s

    def sub_style(self) -> str:
        s = "{\n"
        for k, v in self.style_dict.items():
            if not v:
                continue
            s += f"    {k}: {v};\n"

        if not s.endswith(';\n'):
            return ''

        return s + "}"
