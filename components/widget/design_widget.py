# coding:utf-8
from PyQt5.QtWidgets import QFrame
from qfluentwidgets import ScrollArea

from components.widget.from_widget import FromWidget
from components.widget.table_widget import TableWidget
from components.widget.background_widget import BackgroundWidget
from components.widget.content_widget import ContentWidget
from common.message_util import MessageUtil
from common.style_sheet import StyleSheet


class DesignWidget(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QFrame()
        self.backgroundWidget = BackgroundWidget(self.view)
        self.contentWidget = ContentWidget(parent=self.backgroundWidget)
        self.contentWidget.move(100, 100)
        self.setWidget(self.backgroundWidget)

        self.currentSelectedWidget = None

    def initContentWidget(self, menuWidget: FromWidget, dbTemplate: dict = None):
        """ 初始化纸张模型 """
        widgetList = self.contentWidget.designInitWidget(menuWidget, dbTemplate)
        if widgetList:
            for widget in widgetList:
                widget.checked.connect(self.__onWidgetChecked)

    def setContentWidgetMargin(self, left: int = None, right: int = None, top: int = None, bottom: int = None):
        """ 设置纸张 上下左右边距"""
        if left:
            self.contentWidget.setLeftMargin(left)

        if right:
            self.contentWidget.setRightMargin(right)

        if top:
            self.contentWidget.setTopMargin(top)

        if bottom:
            self.contentWidget.setBottomMargin(bottom)

    def delCurrentSelectedWidget(self):
        """ 删除选中的Widget """
        if not self.currentSelectedWidget:
            MessageUtil.error(self, '删除失败', '当前没有选中任何控件, 请先鼠标左键点击需要删除的控件.')
            return
        self.currentSelectedWidget.delete()
        self.currentSelectedWidget = None

    def addSimpleEditLabel(self, menuWidget: FromWidget):
        """ 添加普通可编辑的Label """
        label = self.contentWidget.addEditLabel(menuWidget)
        label.checked.connect(self.__onWidgetChecked)

    def addSimpleImage(self, menuWidget: FromWidget):
        """ 添加普通可移动的图片 """
        label = self.contentWidget.addImageLabel(menuWidget)
        label.checked.connect(self.__onWidgetChecked)

    def addSimpleTable(self, menuWidget: FromWidget):
        """ 添加普通可拖动的表格 """
        childList = self.contentWidget.children()
        isTable = False
        for child in childList:
            # 当前页面是否有表格组件 每个页面只能有一个表格组件
            if isinstance(child, TableWidget):
                MessageUtil.error(self, '提示信息', '当前模板中已经存在表格,请编辑它吧~')
                isTable = True
        if not isTable:
            table = self.contentWidget.addTableWidget(menuWidget)
            table.checked.connect(self.__onWidgetChecked)

    def resetContentWidget(self, width: int, height: int, direction: str, paperName: str):
        """
        重新设置纸张参数
        :param width: 宽
        :param height: 高
        :param direction: 打印方向
        :param paperName: 纸张名称
        :return:
        """
        self.contentWidget.resetSize(width, height)
        self.contentWidget.resetDirection(direction)
        self.contentWidget.resetPaperName(paperName)

    def resetContentWidgetSize(self, w: int, h: int):
        """ 重新设置纸张大小 """
        self.contentWidget.resetSize(w, h)

    def setContentWidgetBackgroundImage(self, filePath: str):
        """ 设置纸张背景图 """
        self.contentWidget.setBackgroundImage(filePath)

    def removeContentWidgetBackgroundImage(self):
        """ 移除纸张背景图 """
        self.contentWidget.removeBackgroundImage()

    def getContentWidgetData(self) -> dict:
        """ 获取纸张数据结构 """
        return self.contentWidget.getData()

    def __onWidgetChecked(self, widget):
        """ 记录当前被选中的Widget """
        self.currentSelectedWidget = widget
