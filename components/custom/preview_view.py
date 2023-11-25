# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QFrame
from qfluentwidgets import CommandBar, ScrollArea, FluentIcon, Action
from qframelesswindow import FramelessDialog, StandardTitleBar

from components.custom.printer_server import PrinterServer
from components.widget.content_widget import SimpleContentWidget
from components.widget.background_widget import BackgroundWidget
from common.style_sheet import StyleSheet
from server.service.template_base_service import findByCode

"""
预览页
"""


class PreviewCard(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backgroundWidget = BackgroundWidget(parent)
        self.contentWidget = SimpleContentWidget(parent=self.backgroundWidget)
        self.contentWidget.move(100, 100)
        self.setWidget(self.backgroundWidget)

        self.setObjectName('previewCard')


class PreviewCardView(FramelessDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('previewCardView')
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('预览')
        objectView = QFrame()
        objectView.setObjectName("view")
        layout = QVBoxLayout(self)
        self.titleCommand = CommandBar(objectView)
        self.contentWidget = PreviewCard(objectView)

        layout.setContentsMargins(6, 45, 6, 12)
        layout.setSpacing(6)
        layout.addWidget(self.titleCommand)
        layout.addWidget(self.contentWidget)

        # 设置标题栏
        title = StandardTitleBar(self)
        title.setTitle(self.tr('预览'))
        title.setIcon(QIcon(':/gallery/images/logo.png'))
        StyleSheet.LABEL.apply(title.titleLabel)
        self.setTitleBar(title)
        self.titleBar.maxBtn.hide()
        self.titleBar.minBtn.hide()
        self.titleBar.raise_()

        self.initLayout()
        StyleSheet.DIALOG.apply(self)
        self.setFixedSize(850, 900)

    def initLayout(self):
        # command
        self.titleCommand.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        printAction = Action(FluentIcon.PRINT, self.tr('打印'))
        printAction.triggered.connect(self.__onPrintActionChanged)
        downloadAction = Action(FluentIcon.DOWNLOAD, self.tr('下载'))
        downloadAction.triggered.connect(self.__onDownloadAction)
        self.titleCommand.addActions([
            printAction,
            downloadAction
        ])

    def __onPrintActionChanged(self):
        if self.priter:
            self.priter.printWidget()

    def __onDownloadAction(self):
        if self.priter:
            self.priter.downloadWidget()

    def copyContentWidget(self, contentWidget: SimpleContentWidget):
        """
        将传入的widget的子控件全部拷贝到 预览页的contentWidget
        :param contentWidget:
        :return:
        """
        content = self.contentWidget.contentWidget
        content.clone_(contentWidget)
        self.priter = PrinterServer(content)

    def initContentWidget(self, data: dict):
        templateCode = data['templateCode']
        dbTemplate = findByCode(templateCode)
        if not dbTemplate:
            return
        content = self.contentWidget.contentWidget
        content.previewInitWidget(dbTemplate, data)
        self.priter = PrinterServer(content, data)
