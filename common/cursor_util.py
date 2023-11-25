# coding: utf-8
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, Qt


class CursorUtil:

    @staticmethod
    def cursor_style(widget: QWidget, pos: QPoint):
        '''
        设置鼠标样式
        :param widget:
        :param pos:
        :return:
        '''
        # 获取鼠标相对于控件的位置
        mouse_pos = pos
        width = widget.width()
        height = widget.height()
        # 判断鼠标位置是否在边界
        on_left_edge = mouse_pos.x() <= 3
        on_right_edge = mouse_pos.x() >= width - 3
        on_top_edge = mouse_pos.y() <= 3
        on_bottom_edge = mouse_pos.y() >= height - 3
        if on_left_edge or on_right_edge:
            # 设置左右箭头形状
            widget.setCursor(Qt.SizeHorCursor)
        elif on_top_edge or on_bottom_edge:
            # 设置上下箭头形状
            widget.setCursor(Qt.SizeVerCursor)
        else:
            # 设置小手形状
            widget.setCursor(Qt.PointingHandCursor)
