# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import Dialog, CheckBox
from config.config import cfg


class MessageDialog(Dialog):

    def __init__(self, parent=None):
        super().__init__(title='', content='最小化到系统托盘', parent=parent)
        self.windowTitleLabel.setVisible(True)
        self.windowTitleLabel.hide()
        self.titleLabel.hide()

        self.view = QWidget()
        self.view.setObjectName("view")
        self.checkBox = CheckBox(self.tr('不再提醒'), self)
        self.checkBox.toggled.connect(self.__onCheckBoxToggled)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 12, 12, 22)
        layout.setSpacing(0)
        layout.addWidget(self.checkBox, 1, Qt.AlignLeft)

        self.vBoxLayout.insertLayout(2, layout)

    def __onCheckBoxToggled(self, isCheck: bool):
        cfg.set(cfg.isRemind, not isCheck)
