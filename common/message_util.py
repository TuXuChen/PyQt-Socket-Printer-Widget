# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import InfoBar, InfoBarPosition


class MessageUtil:

    @staticmethod
    def error(this: QWidget, title: str, content: str, position: InfoBarPosition = InfoBarPosition.TOP_RIGHT):
        InfoBar.error(
            title=this.tr(title),
            content=this.tr(content),
            orient=Qt.Horizontal,
            isClosable=True,
            position=position,
            duration=-1,
            parent=this
        )

    @staticmethod
    def success(this: QWidget, title: str, content: str, position: InfoBarPosition = InfoBarPosition.TOP_RIGHT, duration: int = 3000):
        InfoBar.success(
            title=this.tr(title),
            content=this.tr(content),
            orient=Qt.Horizontal,
            isClosable=True,
            position=position,
            duration=duration,
            parent=this
        )
