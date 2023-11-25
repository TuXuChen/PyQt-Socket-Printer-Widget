# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import themeColor

"""
背景
"""


class BackgroundWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("backgroundWidget")

        self.setFixedSize(3000, 3000)

    def paintEvent(self, evt):
        """
        绘制网格线
        :param evt:
        :return:
        """
        super().paintEvent(evt)
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)

        pen = QPen()
        color = themeColor()
        color.setAlpha(100)
        pen.setColor(color)
        painter.setPen(pen)
        # 画横向网格线
        for i in range(0, self.height(), 30):
            painter.drawLine(0, i, self.width(), i)
        # 画纵向网格线
        for i in range(0, self.width(), 30):
            painter.drawLine(i, 0, i, self.height())