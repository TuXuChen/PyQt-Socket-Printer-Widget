# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget
from qfluentwidgets import ImageLabel as FluentImageLabel

from components.label.edit_label import EditLabel
from components.label.image_label import ImageLabel
from components.widget.from_widget import FromWidget
from components.widget.table_widget import TableWidget
from server.context.template_context import TemplateContext, TemplateType

"""
纸张内容Widget
"""


class SimpleContentWidget(QWidget):

    def __init__(self, w: int = 210, h: int = 297,
                 left: int = 30, right: int = 30, top: int = 30, bottom: int = 30,
                 direction: str = '纵向打印', paperName: str = 'A4', backgroundImage=None, parent=None):
        """
        纸张模型构造函数
        :param w: 宽度
        :param h: 高度
        :param left: 左边距
        :param right: 右边距
        :param top: 上边距
        :param bottom: 下边距
        :param parent: 父控件
        :param direction: 打印方向
        :param paperName: 纸张名称
        :param backgroundImage: 图片
        """
        super().__init__(parent)
        self.setContentsMargins(left, top, right, bottom)
        self.paperWidth = w
        self.paperHeight = h
        self.direction = direction
        self.paperName = paperName
        # 背景图片文件路径
        self.backgroundImageFilePath = backgroundImage
        # 设置右侧模板宽高 和 滚动条宽高
        a4_w = w * 4
        a4_h = h * 4
        self.resize(a4_w, a4_h)
        self.setObjectName("contentWidget")

    def designInitWidget(self, menuWidget: FromWidget, dbTemplate: dict = None, renderData: dict = None) -> list:
        """ 初始化基础信息 """
        for child in self.children():
            child.deleteLater()

        widgetList = []
        if not dbTemplate:
            return widgetList

        self.setContentsMargins(dbTemplate['left_margin'], dbTemplate['top_margin'], dbTemplate['right_margin'],
                                dbTemplate['bottom_margin'])
        self.paperWidth = dbTemplate['paper_width']
        self.paperHeight = dbTemplate['paper_height']
        self.direction = dbTemplate['direction']
        self.paperName = dbTemplate['paper_name']
        self.backgroundImageFilePath = dbTemplate['background_image']
        self.resetSize(self.paperWidth, self.paperHeight)
        self.update()

        if not dbTemplate:
            return widgetList
        templateCode = dbTemplate['code']
        # 渲染字控件
        labelList = TemplateContext.loadStructure(templateCode, TemplateType.LABEL, renderData)
        for dbLabel in labelList:
            label = EditLabel(text='双击编辑,按回车确定', menuWidget=menuWidget, parent=self)
            label.rendering(dbLabel)
            widgetList.append(label)

        # 渲染图片
        imageList = TemplateContext.loadStructure(templateCode, TemplateType.IMAGE, renderData)
        for dbImage in imageList:
            image = ImageLabel(menuWidget=menuWidget, parent=self)
            image.rendering(dbImage)
            widgetList.append(image)

        # 渲染表格
        tableList = TemplateContext.loadStructure(templateCode, TemplateType.TABLE, renderData)
        if tableList:
            table = TableWidget(menuWidget=menuWidget, parent=self)
            table.rendering(tableList)
            widgetList.append(table)
        return widgetList

    def previewInitWidget(self, dbTemplate: dict = None, renderData: dict = None):
        widgetList = self.designInitWidget(self, dbTemplate, renderData)
        for widget in widgetList:
            if isinstance(widget, EditLabel):
                self.copySimpleLabel(widget)
            elif isinstance(widget, ImageLabel):
                self.copySimpleImage(widget)
            elif isinstance(widget, TableWidget):
                self.copySimpleTable(widget)

            widget.deleteLater()

    def paintEvent(self, evt) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        # 在窗口中绘制背景图像
        if self.backgroundImageFilePath:
            background_image = QPixmap(self.backgroundImageFilePath)
            painter.drawPixmap(0, 0, self.width(), self.height(), background_image)

    def setLeftMargin(self, left: int):
        margin = self.contentsMargins()
        margin.setLeft(left)
        self.setContentsMargins(margin)
        self.update()

    def setRightMargin(self, right: int):
        margin = self.contentsMargins()
        margin.setRight(right)
        self.setContentsMargins(margin)
        self.update()

    def setTopMargin(self, top: int):
        margin = self.contentsMargins()
        margin.setTop(top)
        self.setContentsMargins(margin)
        self.update()

    def setBottomMargin(self, bottom: int):
        margin = self.contentsMargins()
        margin.setBottom(bottom)
        self.setContentsMargins(margin)
        self.update()

    def setBackgroundImage(self, filePath: str):
        """ 设置背景图片 """
        self.backgroundImageFilePath = filePath
        self.update()

    def removeBackgroundImage(self):
        """ 移除背景图 """
        self.backgroundImageFilePath = None
        self.update()

    def resetWidget(self, w: int = 210, h: int = 297,
                    left: int = 30, right: int = 30, top: int = 30, bottom: int = 30,
                    direction: str = '纵向打印', paperName: str = 'A4', backgroundImage=None):
        self.setContentsMargins(left, top, right, bottom)
        self.paperWidth = w
        self.paperHeight = h
        self.direction = direction
        self.paperName = paperName
        # 背景图片文件路径
        self.backgroundImageFilePath = backgroundImage
        # 设置右侧模板宽高 和 滚动条宽高
        a4_w = w * 4
        a4_h = h * 4
        self.resize(a4_w, a4_h)

    def resetSize(self, w: int, h: int):
        """ 重新设置大小 """
        self.paperWidth = w
        self.paperHeight = h
        old_w = self.width()
        old_h = self.height()
        a4_w = w * 4
        a4_h = h * 4
        self.resize(a4_w, a4_h)
        self.adjustChildPosition(old_w, old_h)

    def resetDirection(self, direction: str):
        """ 重新设置打印方向 """
        self.direction = direction

    def resetPaperName(self, paperName: str):
        """ 重新设置纸张名称 """
        self.paperName = paperName

    def adjustChildPosition(self, old_w: int, old_h: int):
        """ 调整纸张内的子控件位置 """
        childList = self.children()
        n_w = self.width()
        n_h = self.height()
        w_ratio = n_w / old_w
        h_ratio = n_h / old_h
        for child in childList:
            if isinstance(child, EditLabel) or isinstance(child, ImageLabel):
                child.move(int(child.x() * w_ratio), int(child.y() * h_ratio))
                child.resize(int(child.width() * w_ratio), int(child.height() * h_ratio))
            if isinstance(child, TableWidget):
                margins = self.contentsMargins()
                child.resize(self.width() - (margins.right() + margins.left()) - 4,
                             int(child.height() * h_ratio))
                child.move(margins.left() + 2, int(child.y() * h_ratio))

    def addEditLabel(self, menuWidget) -> EditLabel:
        """
        添加可编辑的label
        :param menuWidget:
        :return:
        """
        label = EditLabel(text='双击编辑,按回车确定', menuWidget=menuWidget, parent=self)
        label.move(self.width() // 2, 40)
        label.show()

        return label

    def addImageLabel(self, menuWidget) -> ImageLabel:
        """
        添加可移动的图片
        :param menuWidget:
        :return:
        """
        label = ImageLabel(menuWidget=menuWidget, parent=self)
        label.move(self.width() // 4 - 60, 120)
        label.show()

        return label

    def addTableWidget(self, menuWidget) -> TableWidget:
        """
        添加自定义表格
        :param menuWidget:
        :return:
        """
        table = TableWidget(menuWidget=menuWidget, parent=self)
        table.move(self.contentsMargins().left() + 2, self.height() // 4)
        table.show()

        return table

    def clone_(self, oldContent: QWidget):
        """
        克隆
        :param oldContent:
        :return:
        """
        width = oldContent.width()
        height = oldContent.height()
        margins = oldContent.contentsMargins()
        self.resize(width, height)
        self.setContentsMargins(margins)
        # 基本设置
        self.backgroundImageFilePath = oldContent.backgroundImageFilePath
        self.paperWidth = oldContent.paperWidth
        self.paperHeight = oldContent.paperHeight
        self.direction = oldContent.direction
        self.paperName = oldContent.paperName

        for child in oldContent.children():
            if isinstance(child, EditLabel):
                self.copySimpleLabel(child)
            elif isinstance(child, ImageLabel):
                self.copySimpleImage(child)
            elif isinstance(child, TableWidget):
                self.copySimpleTable(child)

    def copySimpleLabel(self, editLabel: EditLabel):
        """
        将可编辑的label复制成普通QLabel
        :param editLabel:
        :return:
        """
        label = QLabel(self)
        editLabel.clone_(label)

    def copySimpleImage(self, imageLabel: ImageLabel):
        """
        将图片复制成普通FluentImageLabel
        :param imageLabel:
        :return:
        """
        image = FluentImageLabel(self)
        imageLabel.clone_(image)

    def copySimpleTable(self, tableWidget: TableWidget):
        """
        将表格复制成普通的QTableWidget
        :param tableWidget:
        :return:
        """
        table = QTableWidget(self)
        tableWidget.clone_(table)

    def getData(self) -> dict:
        """
        获取数据结构
        :return:
        """
        result = {}
        paperInfo = {
            'paperWidth': self.paperWidth,
            'paperHeight': self.paperHeight,
            'backgroundImage': self.backgroundImageFilePath,
            'direction': self.direction,
            'paperName': self.paperName,
            'leftMargin': self.contentsMargins().left(),
            'topMargin': self.contentsMargins().top(),
            'rightMargin': self.contentsMargins().right(),
            'bottomMargin': self.contentsMargins().bottom()
        }
        result['paperInfo'] = paperInfo
        labelList = []
        imageList = []
        tableList = []
        for child in self.children():
            if isinstance(child, EditLabel):
                labelData = child.getData()
                labelList.append(labelData)
            elif isinstance(child, ImageLabel):
                imageData = child.getData()
                imageList.append(imageData)
            elif isinstance(child, TableWidget):
                tableList = child.getData()

        result['labelList'] = labelList
        result['imageList'] = imageList
        result['tableList'] = tableList
        return result


"""
具有边框线的纸张Widget
"""


class ContentWidget(SimpleContentWidget):

    def paintEvent(self, evt):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        pen = QPen(QColor(100, 100, 100), 1, Qt.SolidLine)
        painter.setPen(pen)

        margin = self.contentsMargins()
        # 上边距线
        painter.drawLine(margin.left(), margin.top(), self.width() - margin.right(), margin.top())
        # 下边距线
        painter.drawLine(margin.left(), self.height() - margin.bottom(), self.width() - margin.right(),
                         self.height() - margin.bottom())
        # 左边距线
        painter.drawLine(margin.left(), margin.top(), margin.left(), self.height() - margin.top())
        # 右边距线
        painter.drawLine(self.width() - margin.right(), margin.top(), self.width() - margin.right(),
                         self.height() - margin.bottom())
        # 在窗口中绘制背景图像
        if self.backgroundImageFilePath:
            background_image = QPixmap(self.backgroundImageFilePath)
            painter.drawPixmap(0, 0, self.width(), self.height(), background_image)
