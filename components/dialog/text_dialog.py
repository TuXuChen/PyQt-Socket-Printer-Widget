# coding:utf-8
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import Dialog, TextEdit


class TextDialogView(Dialog):

    def __init__(self, title: str, content: str, parent=None):
        super().__init__(title=title, content='', parent=parent)
        self.windowTitleLabel.setVisible(True)
        self.contentLabel.hide()
        self.titleLabel.hide()
        self.textLayout.setContentsMargins(12, 12, 12, 12)
        self.textLayout.setSpacing(5)
        self.yesButton.setText(self.tr('确定'))
        self.cancelButton.setText(self.tr('取消'))

        self.view = QWidget()
        self.view.setObjectName("view")
        self.text = TextEdit(self)
        self.text.setMarkdown(content)
        self.text.setReadOnly(True)
        self.text.setMinimumHeight(200)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(0)
        layout.addWidget(self.text)

        self.vBoxLayout.insertLayout(2, layout)
        self.setFixedWidth(270)
