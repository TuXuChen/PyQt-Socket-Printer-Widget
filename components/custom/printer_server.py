# coding:utf-8
from typing import List

from PyQt5.QtCore import QSizeF, Qt, QSize
from PyQt5.QtGui import QPageSize, QPainter, QImage, QPixmap
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QLabel, QTableWidget, QWidget

from common.message_util import MessageUtil
from common.random_util import getRandom
from components.widget.content_widget import SimpleContentWidget
from components.label.edit_label import PrinterParameterEnum
from components.widget.table_widget import renderTable
from config.config import cfg
from server.service.template_table_service import findByTemplateCode
from server.context.template_context import TemplateContext, TemplateType

"""
打印服务
"""


class PrinterServer:

    def __init__(self, contentWidget: SimpleContentWidget, data: dict = None):
        self.parent = contentWidget
        # 基本参数
        self.backgroundImageFilePath = contentWidget.backgroundImageFilePath
        self.paperWidth = contentWidget.paperWidth
        self.paperHeight = contentWidget.paperHeight
        # 分页参数
        self.currentPage = 1
        self.totalPage = 1
        self.templateCode = None
        if data:
            self.templateCode = data['templateCode']
            dbTable = findByTemplateCode(self.templateCode)
            if dbTable and data['list']:
                tableList = data['list']
                table = dbTable[0]
                row = table['row_count']
                self.totalPage = len(tableList) // row + (1 if len(tableList) % row > 0 else 0)

        self.renderData = data

    def printWidget(self):
        """ 打印当前Widget """
        printer = QPrinter()
        printDialog = QPrintDialog(printer, self.parent)
        printDialog.setOptions(QPrintDialog.PrintToFile | QPrintDialog.PrintSelection)
        if printDialog.exec_() == QPrintDialog.Accepted:
            self.__RenderingPaper(printer)
            MessageUtil.success(self.parent, self.parent.tr('打印成功!'), self.parent.tr(''))

    def downloadWidget(self):
        """ 下载当前Widget """
        defaultFilename = '\预览模板' + getRandom() + '.pdf'
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(cfg.downloadFolder.value + defaultFilename)
        self.__RenderingPaper(printer)
        MessageUtil.success(self.parent, self.parent.tr('下载PDF'), self.parent.tr(f'下载成功!已经存放在{cfg.downloadFolder.value}'))

    def __RenderingPaper(self, printer: QPrinter):
        """ 渲染纸张 """
        printer.setPageSize(QPageSize(QSizeF(self.paperWidth, self.paperHeight), QPageSize.Millimeter))
        printer.setPaperSize(QSizeF(self.paperWidth, self.paperHeight), QPrinter.Millimeter)
        printer.setFullPage(False)
        painter = QPainter(printer)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        # 偏移量
        shiftingW = printer.width() / self.parent.width()
        shiftingH = printer.height() / self.parent.height()
        firstWidget = []
        everyWidget = []
        lastWidget = []
        for child_widget in self.parent.children():
            if isinstance(child_widget, QLabel):
                printerType = child_widget.property('printer_type')
                if printerType == PrinterParameterEnum.FIRST.value:
                    firstWidget.append(child_widget)
                elif printerType == PrinterParameterEnum.LAST.value:
                    lastWidget.append(child_widget)
                else:
                    everyWidget.append(child_widget)

            if isinstance(child_widget, QTableWidget):
                everyWidget.append(child_widget)

        # 如果有背景图
        self.__createPage(printer, painter)
        # 渲染子控件
        self.__printerPixmap(painter, firstWidget, shiftingW, shiftingH)
        if self.totalPage != 1:
            for page in range(1, self.totalPage + 1):
                self.__printerPixmap(painter, everyWidget, shiftingW, shiftingH, page)
                if page == self.totalPage:
                    self.__printerPixmap(painter, lastWidget, shiftingW, shiftingH, page)
                else:
                    self.__createPage(printer, painter, True)
        else:
            self.__printerPixmap(painter, everyWidget, shiftingW, shiftingH)
            self.__printerPixmap(painter, lastWidget, shiftingW, shiftingH)
        # 绘制结束
        painter.end()
        # 如果有表格 需要还原数据 确保页面内容不发生改变
        for widget in everyWidget:
            if isinstance(widget, QTableWidget):
                self.__loadTable(widget)

    def __loadTable(self, widget: QTableWidget, currentPage: int = 1):
        if self.templateCode:
            widget.clearContents()
            data = TemplateContext.loadStructure(self.templateCode, TemplateType.TABLE, self.renderData, currentPage)
            renderTable(widget, data)

    def __createPage(self, printer: QPrinter, painter: QPainter, isCreate: bool = False):
        if isCreate:
            printer.newPage()
        # 如果有背景图
        if self.backgroundImageFilePath:
            backgroundImage = QImage(self.backgroundImageFilePath)
            backgroundImage = backgroundImage.scaled(printer.width(), printer.height())
            painter.drawImage(0, 0, backgroundImage)

    def __printerPixmap(self, painter: QPainter, widgets: List[QWidget], shiftingW: float, shiftingH: float, currentPage: int = 1):
        """
        绘制图像
        :param painter: 画笔
        :param widgets: 需要绘制的控件
        :param shiftingW: 横偏移
        :param shiftingH: 纵偏移
        :param currentPage: 当前页号
        :return:
        """
        pixelRatio = painter.device().devicePixelRatioF()
        for widget in widgets:
            if isinstance(widget, QTableWidget):
                self.__loadTable(widget, currentPage)

            child_rect = widget.geometry()
            pixmap = QPixmap(child_rect.size())
            widget.render(pixmap)
            size = QSize(int(child_rect.width() * shiftingW * pixelRatio),
                         int(child_rect.height() * shiftingH * pixelRatio))
            pixmap = pixmap.scaled(size, aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
            painter.drawPixmap(int(child_rect.x() * shiftingW), int(child_rect.y() * shiftingH), pixmap)
