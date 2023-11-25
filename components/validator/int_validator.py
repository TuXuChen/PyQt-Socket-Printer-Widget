# coding:utf-8
import re
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from qfluentwidgets import ConfigValidator


class IntValidator(QRegExpValidator):

    def __init__(self, regex: str = "^(1|[1-9][0-9]?)$", parent=None):
        # 创建正则表达式，限制只能输入 0-99 之间的整数
        regex = QRegExp(regex)
        super().__init__(regex, parent)


class IntConfigValidator(ConfigValidator):

    def __init__(self, default):
        self.default = default
        self.pattern = re.compile(r'^[1-9]\d{0,3}$')

    def validate(self, value):
        if self.pattern.match(str(value)):
            return True
        else:
            return False

    def correct(self, value):
        return value if self.validate(str(value)) else self.default
