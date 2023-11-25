# coding:utf-8
from qfluentwidgets import SearchLineEdit


class SimpleSearchLineEdit(SearchLineEdit):

    def __init__(self, placeholderText: str, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr(placeholderText))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)