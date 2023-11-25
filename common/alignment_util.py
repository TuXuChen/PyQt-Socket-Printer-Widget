from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

'''
对齐方式工具类
'''


class AlignmentUtil:

    @staticmethod
    def get_alignment_text(widget: QWidget = None, alignment: int = None):
        try:
            if widget:
                alignment = widget.alignment()
            if int(alignment) == 129:
                return "左对齐"
            elif int(alignment) == 130:
                return "右对齐"
            elif int(alignment) == 132:
                return "居中对齐"
            elif int(alignment) == 0:
                return "左对齐"
            else:
                return ""
        except Exception as e:
            raise RuntimeError("当前widget没有alignment()方法")

    @staticmethod
    def get_alignment(alignment: int):
        if alignment == 129:
            return Qt.AlignVCenter | Qt.AlignLeft
        elif alignment == 130:
            return Qt.AlignVCenter | Qt.AlignRight
        elif alignment == 132:
            return Qt.AlignCenter
        elif alignment == 0:
            return Qt.AlignVCenter | Qt.AlignLeft
        return Qt.AlignCenter
