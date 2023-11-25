# coding:utf-8
import os
from enum import Enum
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

from components.widget.move_widget import MoveSizeQWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from components.widget.from_widget import FromWidget
from common.style_util import StyleUtil
from common.alignment_util import AlignmentUtil
from common.file_util import readResourceFile

"""
可编辑移动的QLabel
"""


class ColorEnum(Enum):
    """ 颜色枚举 """
    COLOR_BLACK = "black"
    COLOR_YELLOW = "yellow"


class BorderEnum(Enum):
    """ 边框枚举 """
    BORDER_TOP = 1
    BORDER_BOTTOM = 2
    BORDER_ALL = 0
    BORDER_NONE = 3


class PrinterParameterEnum(Enum):
    """打印参数"""
    FIRST = 0
    EVERY = 1
    LAST = 2


def getQssFile() -> str:
    """ 获取QSS路径 """
    filePath = ':/gallery/qss/edit_label.qss'
    content = readResourceFile(filePath)
    return content


# 打印参数
printerParameterData = [
    {"第一页打印": {"printer_type": PrinterParameterEnum.FIRST.value}},
    {"每页打印": {"printer_type": PrinterParameterEnum.EVERY.value}},
    {"最后一页打印": {"printer_type": PrinterParameterEnum.LAST.value}}
]

# 显示边框
borderShowData = [
    {"全部显示": {"border": "all"}},
    {"显示仅上边框": {"border": "top"}},
    {"显示仅下边框": {"border": "bottom"}},
    {"无边框": {"border": "None"}}
]

# 边框类型 实线 虚线
borderTypeData = [{"实线": {"border_type": "solid"}}, {"虚线": {"border_type": "dashed"}}]

# 对齐方式
fontAlignmentData = [
    {"左对齐": {"alignment": Qt.AlignVCenter | Qt.AlignLeft}},
    {"居中对齐": {"alignment": Qt.AlignCenter}},
    {"右对齐": {"alignment": Qt.AlignVCenter | Qt.AlignRight}}]


class EditLabel(MoveSizeQWidget):

    checked = pyqtSignal(QWidget)

    def __init__(self, text: str, menuWidget: FromWidget, parent: QWidget = None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setToolTip(self.tr("双击鼠标进入编辑模式, 按回车键结束编辑模式"))
        self.menuWidget = menuWidget

        layout = QVBoxLayout(self)
        self.label = QLabel(text, self)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setText(text)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.lineEdit.hide()

        self.setObjectName("editLabel")
        self.resize(120, 40)
        style = getQssFile()
        border_size = 1
        border_type = "solid"
        style = style.replace("@border_size@", str(border_size)).replace("@border_type@", border_type)
        self.setStyleSheet(style)
        self.setProperty("border_size", border_size)
        self.setProperty("border_type", border_type)
        self.setProperty('color', ColorEnum.COLOR_BLACK.value)
        self.setProperty('border', BorderEnum.BORDER_ALL.value)
        self.setProperty('printer_type', PrinterParameterEnum.FIRST.value)
        self.lineEdit.textChanged.connect(self.__onTextChanged)
        self.lineEdit.editingFinished.connect(self.__onEditingFinished)

    def mousePressEvent(self, evt) -> None:
        """ 鼠标单击事件 """
        if evt.button() == Qt.LeftButton:
            self.setFocus()
            if self.property('color') is not None and self.property('color') == ColorEnum.COLOR_YELLOW.value:
                return super().mousePressEvent(evt)
            self.setProperty('color', ColorEnum.COLOR_YELLOW.value)
            StyleUtil.refresh_style(self)  # 重新设置样式
            # 选中信号
            self.checked.emit(self)
            # 初始化操作菜单
            self.initMenuWidget()
        return super().mousePressEvent(evt)

    def focusOutEvent(self, evt) -> None:
        """ 失去焦点事件 """
        if self.lineEdit.isModified():
            return super().focusOutEvent(evt)
        self.setProperty('color', ColorEnum.COLOR_BLACK.value)
        StyleUtil.refresh_style(self) # 重新设置样式
        return super().focusOutEvent(evt)

    def mouseDoubleClickEvent(self, evt) -> None:
        """ 鼠标双击事件 """
        self.label.hide()
        self.lineEdit.show()
        self.lineEdit.setModified(True)
        self.lineEdit.setFocus()
        return super().mouseDoubleClickEvent(evt)

    def __onTextChanged(self, text: str):
        self.label.setText(text)
        self.lineEdit.setText(text)

    def __onEditingFinished(self):
        self.lineEdit.setModified(False)
        self.lineEdit.clearFocus()
        self.lineEdit.hide()
        self.label.show()
        self.setFocus()
        self.clearFocus()

    def delete(self):
        """ 删除控件 """
        self.menuWidget.delViewLater()
        self.menuWidget.addPromptText("请选中右侧的控件")
        self.deleteLater()

    def rendering(self, data: dict):
        """ 渲染控件 """
        self.setProperty("printer_type", data['printer_type'])
        self.label.setText(data['value'])
        self.lineEdit.setText(data['value'])
        font = self.label.font()
        font.setPointSize(data['font_size'])
        font.setFamily(data['font_family'])
        font.setItalic(False if data['font_italic'] == 0 else True)
        font.setBold(False if data['font_bold'] == 0 else True)
        font.setUnderline(False if data['font_underline'] == 0 else True)
        self.label.setFont(font)
        palette = self.label.palette()
        palette.setColor(self.label.foregroundRole(), QColor(data['font_color']))
        self.label.setPalette(palette)
        self.setProperty("border_size", data['border_size'])
        self.setProperty("border_type", data['border_type'])
        self.setProperty("color", "black")
        self.setProperty("border", data['border'])
        self.label.setAlignment(AlignmentUtil.get_alignment(data['font_alignment']))
        self.resize(data['width'], data['height'])
        self.move(data['x_coordinate'], data['y_coordinate'])
        self.update()

    def getData(self) -> dict:
        """ 获取数据结构 """
        data = {
            'value': self.label.text(),
            'printerType': self.property('printer_type'),
            'border': self.property('border'),
            'borderSize': self.property('border_size'),
            'borderType': self.property('border_type'),
            'width': self.width(),
            'height': self.height(),
            'xCoordinate': self.x(),
            'yCoordinate': self.y(),
            'fontSize': self.label.font().pointSize(),
            'fontFamily': self.label.font().family(),
            'fontColor': self.label.palette().color(self.label.foregroundRole()).name(),
            'fontItalic': self.label.font().italic(),
            'fontBold': self.label.font().bold(),
            'fontUnderline': self.label.font().underline(),
            'fontAlignment': int(self.label.alignment())
        }
        return data

    def clone_(self, label: QLabel):
        """
        克隆
        """
        label.setObjectName('editLabel')
        label.setAttribute(Qt.WA_StyledBackground, True)
        label.setText(self.label.text())
        label.setFont(self.label.font())
        label.setPalette(self.label.palette())
        label.setStyleSheet(self.styleSheet())
        label.setProperty("border_size", self.property("border_size"))
        label.setProperty("border_type", self.property("border_type"))
        label.setProperty("color", "black")
        label.setProperty("border", self.property("border"))
        label.setProperty("printer_type", self.property("printer_type"))
        label.setAlignment(self.label.alignment())
        label.resize(self.width(), self.height())
        label.move(self.x(), self.y())

    def initMenuWidget(self):
        self.menuWidget.delAll()
        self.menuWidget.addLabelCard(self.tr('基础设置'))
        # 打印参数
        self.printerParameterWidget = self.menuWidget.addComboBoxCard(self.tr('打印参数:'),
                                                                      printerParameterData,
                                                                      currentIndex=self.property("printer_type"),
                                                                      callback=self.__onPrinterParameterWidgetChanged)
        # 显示边框
        self.borderShowWidget = self.menuWidget.addComboBoxCard(self.tr('显示边框:'), borderShowData,
                                                                currentIndex=self.property("border"),
                                                                callback=self.__onBorderShowWidgetChanged)
        # 边框类型 实线 虚线
        is_current_border_type = 0 if self.property("border_type") == "solid" else 1
        self.borderTypeWidget = self.menuWidget.addComboBoxCard(self.tr('边框类型:'), borderTypeData,
                                                                currentIndex=is_current_border_type,
                                                                callback=self.__onBorderTypeWidgetChanged)
        # 边框粗细
        self.borderSizeWidget = self.menuWidget.addSliderCard(self.tr('边框粗细:'), 1, 10,
                                                              self.property("border_size"),
                                                              self.__onBorderSizeWidgetReleased)
        # 边框宽度
        self.borderWidthWidget = self.menuWidget.addSliderCard(self.tr('边框宽度:'), 0, 200,
                                                               self.width(), self.__onBorderWidthWidgetReleased)
        # 边框高度
        self.borderHeightWidget = self.menuWidget.addSliderCard(self.tr('边框高度:'), 20, 200,
                                                                self.height(), self.__borderHeightWidgetReleased)
        self.menuWidget.addLabelCard(self.tr('布局设置'))
        self.menuWidget.addPushButton(self.tr('置于上方:'), self.tr('选泽'), self.tr('点击将控件放置在上方'),
                                      lambda: self.raise_())
        self.menuWidget.addPushButton(self.tr('置于下方:'), self.tr('选泽'), self.tr('点击将控件放置在下方'),
                                      lambda: self.lower())
        self.menuWidget.addLabelCard(self.tr('字体设置'))
        # 字体大小
        self.fontSizeWidget = self.menuWidget.addSliderCard(self.tr('字体大小:'), 5, 30,
                                                            self.label.font().pointSize(),
                                                            self.__onFontSizeWidgetReleased)
        # 字体名称
        self.fontFamilyWidget = self.menuWidget.addFontComboBox(self.tr('字体名称:'),
                                                                self.label.font().family(),
                                                                self.__onFontFamilyChanged)
        # 字体颜色
        self.fontColorWidget = self.menuWidget.addColorButtonCard(self.tr('字体颜色:'),
                                                                  self.label.palette().color(self.label.foregroundRole()).name(),
                                                                  self.__onFontColorWidgetChanged)
        # 字体斜体
        self.fontItalicWidget = self.menuWidget.addSwitchButtonCard(self.tr('字体斜体:'),
                                                                    self.label.font().italic(),
                                                                    self.__onFontItalicWidgetChanged)
        # 字体加粗
        self.fontBoldWidget = self.menuWidget.addSwitchButtonCard(self.tr('字体加粗:'),
                                                                  self.label.font().bold(),
                                                                  self.__onFontBoldWidgetChanged)
        # 下划线
        self.fontUnderlineWidget = self.menuWidget.addSwitchButtonCard(self.tr('下划线 :'),
                                                                       self.label.font().underline(),
                                                                       self.__onFontUnderlineWidgetChanged)
        # 对齐方式
        self.fontAlignmentWidget = self.menuWidget.addComboBoxCard(self.tr('对齐方式:'),
                                                                   fontAlignmentData,
                                                                   currentText=AlignmentUtil.get_alignment_text(widget=self.label),
                                                                   callback=self.__onFontAlignmentWidgetChanged)

    def __onPrinterParameterWidgetChanged(self):
        self.setProperty('printer_type', self.printerParameterWidget.currentData()['printer_type'])

    def __onBorderShowWidgetChanged(self, index):
        data = self.borderShowWidget.currentData()
        if data["border"] == "all":
            self.setProperty("border", BorderEnum.BORDER_ALL.value)
        elif data["border"] == "top":
            self.setProperty("border", BorderEnum.BORDER_TOP.value)
        elif data["border"] == "bottom":
            self.setProperty("border", BorderEnum.BORDER_BOTTOM.value)
        elif data["border"] == "None":
            self.setProperty("border", BorderEnum.BORDER_NONE.value)
        StyleUtil.refresh_style(self)

    def __onBorderTypeWidgetChanged(self):
        borderType = self.borderTypeWidget.currentData()["border_type"]
        borderSize = self.property("border_size")
        style = getQssFile()
        style = style.replace("@border_size@", str(borderSize)).replace("@border_type@", borderType)
        self.setStyleSheet(style)
        StyleUtil.refresh_style(self)
        self.setProperty("border_type", borderType)

    def __onBorderSizeWidgetReleased(self):
        borderSize = self.borderSizeWidget.value()
        borderType = self.property("border_type")
        style = getQssFile()
        style = style.replace("@border_size@", str(borderSize)).replace("@border_type@", borderType)
        self.setStyleSheet(style)
        StyleUtil.refresh_style(self)
        self.setProperty("border_size", borderSize)

    def __onBorderWidthWidgetReleased(self):
        width = self.borderWidthWidget.value()
        self.resize(width, self.height())

    def __borderHeightWidgetReleased(self):
        height = self.borderHeightWidget.value()
        self.resize(self.width(), height)

    def __onFontSizeWidgetReleased(self):
        fontSize = self.fontSizeWidget.value()
        font = self.label.font()
        font.setPointSize(fontSize)
        self.label.setFont(font)

    def __onFontFamilyChanged(self, family: str):
        font = self.label.font()
        font.setFamily(family)
        self.label.setFont(font)

    def __onFontColorWidgetChanged(self, color):
        palette = self.label.palette()
        palette.setColor(self.label.foregroundRole(), color)
        self.label.setPalette(palette)

    def __onFontItalicWidgetChanged(self, isChecked: bool):
        font = self.label.font()
        font.setItalic(isChecked)
        self.label.setFont(font)

    def __onFontBoldWidgetChanged(self, isChecked: bool):
        font = self.label.font()
        font.setBold(isChecked)
        self.label.setFont(font)

    def __onFontUnderlineWidgetChanged(self, isChecked: bool):
        font = self.label.font()
        font.setUnderline(isChecked)
        self.label.setFont(font)

    def __onFontAlignmentWidgetChanged(self):
        alignment = self.fontAlignmentWidget.currentData()["alignment"]
        self.label.setAlignment(alignment)
