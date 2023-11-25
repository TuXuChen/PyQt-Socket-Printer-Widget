# coding:utf-8
from typing import Union
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QFormLayout
from qfluentwidgets import ExpandGroupSettingCard, FluentIconBase, LineEdit, PrimaryPushButton
from components.validator.int_validator import IntValidator
from components.validator.ip_validator import IPValidator

"""
IP端口输入卡
"""


class HostEditSettingCard(ExpandGroupSettingCard):
    confirmClicked = pyqtSignal(str, int)

    def __init__(self, defIp: str, defPort: int, icon: Union[str, QIcon, FluentIconBase], title: str, content=None, parent=None):
        super().__init__(icon, title, content, parent=parent)

        self.choiceLabel = QLabel(self)

        self.lineWidget = QWidget(self.view)
        self.lineLayout = QFormLayout(self.lineWidget)
        self.hostLineEdit = LineEdit(self.lineWidget)
        self.hostLineEdit.setPlaceholderText('请输入IP地址')
        self.hostLineEdit.setText(defIp)
        self.portLineEdit = LineEdit(self.lineWidget)
        self.portLineEdit.setPlaceholderText('请输入端口')
        self.portLineEdit.setText(str(defPort))

        self.confirmButtonWidget = QWidget(self.view)
        self.confirmButtonLayout = QHBoxLayout(self.confirmButtonWidget)
        self.confirmLabel = QLabel(self.tr('点击确定后,需要重新开关连接'), self.confirmButtonWidget)
        self.confirmButton = PrimaryPushButton(self.confirmButtonWidget)
        self.confirmButton.setText('确认')

        self.__initWidget()

    def __initWidget(self):
        self.__initLayout()

        self.hostLineEdit.setValidator(IPValidator())
        self.portLineEdit.setValidator(IntValidator(regex="^[1-9]\d{0,3}$"))
        self.confirmButton.clicked.connect(self.__confirmButtonChecked)

    def __initLayout(self):
        self.addWidget(self.choiceLabel)
        self.lineLayout.setSpacing(19)
        self.lineLayout.setAlignment(Qt.AlignLeft)
        self.lineLayout.setContentsMargins(28, 18, 440, 18)

        self.lineLayout.setWidget(0, QFormLayout.LabelRole, QLabel(self.tr('IP地址:'), self.lineWidget))
        self.lineLayout.setWidget(0, QFormLayout.FieldRole, self.hostLineEdit)
        self.lineLayout.setWidget(1, QFormLayout.LabelRole, QLabel(self.tr('端口:'), self.lineWidget))
        self.lineLayout.setWidget(1, QFormLayout.FieldRole, self.portLineEdit)

        self.confirmButtonLayout.setContentsMargins(48, 18, 44, 18)
        self.confirmButtonLayout.addWidget(self.confirmLabel, 0, Qt.AlignLeft)
        self.confirmButtonLayout.addWidget(self.confirmButton, 0, Qt.AlignRight)
        self.confirmButtonLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.viewLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.addGroupWidget(self.lineWidget)
        self.addGroupWidget(self.confirmButtonWidget)

    def __confirmButtonChecked(self):
        self.confirmClicked.emit(self.hostLineEdit.text(), int(self.portLineEdit.text()))
