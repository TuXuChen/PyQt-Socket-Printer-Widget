# coding:utf-8
from enum import Enum
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap
from qfluentwidgets import ImageLabel as FluentImageLabel
from PyQt5.QtWidgets import QWidget, QFileDialog

from components.widget.from_widget import FromWidget
from components.widget.move_widget import SimpleMoveQWidget
from common.file_util import copyImage

"""
可移动的图片
"""


class PrinterParameterEnum(Enum):
    """打印参数"""
    FIRST = 0
    EVERY = 1
    LAST = 2


# 打印参数
printerParameterData = [
    {"第一页打印": {"printer_type": PrinterParameterEnum.FIRST.value}},
    {"每页打印": {"printer_type": PrinterParameterEnum.EVERY.value}},
    {"最后一页打印": {"printer_type": PrinterParameterEnum.LAST.value}}
]

# 设置透明度
opacityEffectData = [
    {"100%": {"opacity": 1}},
    {"70%": {"opacity": 0.7}},
    {"50%": {"opacity": 0.5}},
    {"30%": {"opacity": 0.3}},
    {"0%": {"opacity": 0}},
]


class ImageLabel(SimpleMoveQWidget, FluentImageLabel):
    checked = pyqtSignal(QWidget)

    def __init__(self, menuWidget: FromWidget, parent=None):
        super().__init__(parent)
        self.filePath = ':/gallery/images/logo.png'
        self.setImage(QPixmap(self.filePath))
        self.setToolTip(self.tr('双击上传图片'))
        self.setMinimumSize(50, 50)
        self.resize(50, 50)
        self.menuWidget = menuWidget

        # 透明度
        self.setProperty("opacity", 0)
        # 打印参数
        self.setProperty("printer_type", PrinterParameterEnum.FIRST.value)

    def mousePressEvent(self, evt):
        if evt.button() == Qt.LeftButton:
            # 选中信号
            self.checked.emit(self)
            # 渲染菜单
            self.initMenuWidget()
        # 显式调用父类的 mousePressEvent
        SimpleMoveQWidget.mousePressEvent(self, evt)

    def mouseDoubleClickEvent(self, evt):
        self.__onReplaceImageWidgetChanged()

    def delete(self):
        """ 删除控件 """
        self.menuWidget.delViewLater()
        self.menuWidget.addPromptText("请选中右侧的控件")
        self.deleteLater()

    def rendering(self, data: dict):
        """ 渲染控件 """
        self.setImage(QPixmap(data['value']))
        self.setProperty("printer_type", data['printer_type'])
        self.setFixedSize(data['width'], data['height'])
        self.move(data['x_coordinate'], data['y_coordinate'])
        self.setOpacityEffect(data['opacity'])

    def getData(self) -> dict:
        """ 获取数据结构 """
        data = {
            'value': self.filePath,
            'printerType': self.property('printer_type'),
            'width': self.width(),
            'height': self.height(),
            'xCoordinate': self.x(),
            'yCoordinate': self.y(),
            'opacity': self.getOpacityEffect()
        }
        return data

    def clone_(self, image: FluentImageLabel):
        """
        克隆
        :param image:
        :return:
        """
        oldImage = self.image
        image.setImage(oldImage)
        opacityEffect = QGraphicsOpacityEffect()
        opacityEffect.setOpacity(self.getOpacityEffect())
        image.setGraphicsEffect(opacityEffect)
        image.setProperty("printer_type", self.property("printer_type"))
        image.setFixedSize(self.width(), self.height())
        image.move(self.x(), self.y())

    # 设置透明度值（范围：0-1）
    def setOpacityEffect(self, value: float):
        if value == 1:
            self.setProperty("opacity", 0)
        elif value == 0.7:
            self.setProperty("opacity", 1)
        elif value == 0.5:
            self.setProperty("opacity", 2)
        elif value == 0.3:
            self.setProperty("opacity", 3)
        else:
            self.setProperty("opacity", 4)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(value)
        self.setGraphicsEffect(opacity_effect)
        self.update()

    def getOpacityEffect(self) -> float:
        opacity_effect = self.graphicsEffect()
        if isinstance(opacity_effect, QGraphicsOpacityEffect):
            return opacity_effect.opacity()
        return 1

    def initMenuWidget(self):
        self.menuWidget.delAll()
        self.menuWidget.addLabelCard(self.tr('基础设置'))
        # 打印参数
        self.printerParameterWidget = self.menuWidget.addComboBoxCard(self.tr('打印参数:'),
                                                                      printerParameterData,
                                                                      currentIndex=self.property("printer_type"),
                                                                      callback=self.__onPrinterParameterWidgetChanged)
        # 更换图片
        self.menuWidget.addPushButton(self.tr('更换图片:'), self.tr('选择'),
                                      self.tr('点击选中更换的图片'), self.__onReplaceImageWidgetChanged)
        # 设置宽度
        self.imageWidthWidget = self.menuWidget.addSliderCard(self.tr('设置宽度:'), 50, 500,
                                                              self.size().width(), self.__onImageWidthWidgetReleased)
        # 设置高度
        self.imageHeightWidget = self.menuWidget.addSliderCard(self.tr('设置高度:'), 50, 500,
                                                               self.size().height(), self.__onImageHeightWidgetReleased)
        # 设置透明度
        self.opacityEffectWidget = self.menuWidget.addComboBoxCard(self.tr('设置透明度:'),
                                                                   opacityEffectData,
                                                                   currentIndex=self.property("opacity"),
                                                                   callback=self.__onOpacityEffectWidgetChanged)
        self.menuWidget.addLabelCard(self.tr('布局设置'))
        self.menuWidget.addPushButton(self.tr('置于上方:'), self.tr('选泽'), self.tr('点击将控件放置在上方'),
                                      lambda: self.raise_())
        self.menuWidget.addPushButton(self.tr('置于下方:'), self.tr('选泽'), self.tr('点击将控件放置在下方'),
                                      lambda: self.lower())

    def __onPrinterParameterWidgetChanged(self):
        self.setProperty('printer_type', self.printerParameterWidget.currentData()['printer_type'])

    def __onReplaceImageWidgetChanged(self):
        openFile = QFileDialog.getOpenFileName(self.parentWidget(), '选择图片', './', 'Image(*.png)', 'Image(*.jpg)')
        if openFile and openFile[0]:
            self.filePath = copyImage(openFile[0])
            self.setImage(QPixmap(self.filePath))

    def __onImageWidthWidgetReleased(self):
        size = self.imageWidthWidget.value()
        self.setFixedWidth(size)

    def __onImageHeightWidgetReleased(self):
        size = self.imageHeightWidget.value()
        self.setFixedHeight(size)

    def __onOpacityEffectWidgetChanged(self):
        value = self.opacityEffectWidget.currentData()["opacity"]
        self.setOpacityEffect(value)
