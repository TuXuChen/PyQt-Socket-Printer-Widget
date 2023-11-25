# coding: utf-8
from PyQt5.QtWidgets import QWidget

'''
样式工具类
'''


class StyleUtil:

    @staticmethod
    def refresh_style(widget: QWidget):
        '''
        刷新样式表
        :param widget:
        :return:
        '''
        widget.style().unpolish(widget)  # 取消对该widget的样式设置
        widget.style().polish(widget)  # 重新设置样式
        widget.update()

    @staticmethod
    def set_style(widget: QWidget, style: str):
        '''
        设置样式表
        :param widget:
        :param style:
        :return:
        '''
        widget.setStyleSheet(style)
        StyleUtil.refresh_style(widget)
