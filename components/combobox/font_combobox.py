# coding:utf-8
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import ComboBox

'''
自定义下拉框字体列表
'''


class FontComboBox(ComboBox):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.all_fonts = QFontDatabase().families()
        for font in self.all_fonts:
            self.addItem(font)