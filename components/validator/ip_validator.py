# coding:utf-8
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp


class IPValidator(QRegExpValidator):

    def __init__(self, parent=None):
        regex = QRegExp("([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])(\.([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])){3}$")
        super().__init__(regex, parent)
