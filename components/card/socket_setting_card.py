# coding:utf-8
from typing import Union
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QFormLayout
from qfluentwidgets import ExpandGroupSettingCard, FluentIconBase, LineEdit, PrimaryPushButton


class SocketSettingCard(ExpandGroupSettingCard):
    confirmClicked = pyqtSignal(str)

    def __init__(self, defAddress: str, icon: Union[str, QIcon, FluentIconBase], title: str, content=None, parent=None):
        super().__init__(icon, title, content, parent=parent)
        self.choiceLabel = QLabel(self)

        self.lineWidget = QWidget(self.view)
        self.lineLayout = QFormLayout(self.lineWidget)
        self.addressLineEdit = LineEdit(self.lineWidget)
        self.addressLineEdit.setPlaceholderText('请输入连接地址,格式为 ws://IP或域名:端口（示例ws://127.0.0.1:8080）')
        self.addressLineEdit.setText(defAddress)
        self.addressLineEdit.setToolTip('格式为 ws://IP或域名:端口（示例ws://127.0.0.1:8080）')

        self.confirmButtonWidget = QWidget(self.view)
        self.confirmButtonLayout = QHBoxLayout(self.confirmButtonWidget)
        self.confirmLabel = QLabel(self.tr('点击确定后,需要重新开关连接'), self.confirmButtonWidget)
        self.confirmButton = PrimaryPushButton(self.confirmButtonWidget)
        self.confirmButton.setText('确认')

        self.__initLayout()
        self.confirmButton.clicked.connect(self.__confirmButtonChecked)

    def __initLayout(self):
        self.addWidget(self.choiceLabel)
        self.lineLayout.setSpacing(19)
        self.lineLayout.setAlignment(Qt.AlignLeft)
        self.lineLayout.setContentsMargins(28, 18, 440, 18)

        self.lineLayout.setWidget(0, QFormLayout.LabelRole, QLabel(self.tr('socket地址:'), self.lineWidget))
        self.lineLayout.setWidget(0, QFormLayout.FieldRole, self.addressLineEdit)

        self.confirmButtonLayout.setContentsMargins(48, 18, 44, 18)
        self.confirmButtonLayout.addWidget(self.confirmLabel, 0, Qt.AlignLeft)
        self.confirmButtonLayout.addWidget(self.confirmButton, 0, Qt.AlignRight)
        self.confirmButtonLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.viewLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.addGroupWidget(self.lineWidget)
        self.addGroupWidget(self.confirmButtonWidget)

    def __confirmButtonChecked(self):
        self.confirmClicked.emit(self.addressLineEdit.text())
