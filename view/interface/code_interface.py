# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidgetItem, QAbstractItemView, QFrame, QVBoxLayout
from qfluentwidgets import (PrimaryPushButton, StrongBodyLabel, TableWidget, Dialog)

from components.frame.frame import SimpleFrame
from components.input.line_edit import SimpleSearchLineEdit
from components.dialog.text_dialog import TextDialogView
from view.interface.gallery_interface import GalleryInterface
from server.service.template_base_service import findList, findLikeByName
from server.context.template_context import TemplateContext


class TableFrame(SimpleFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = TableWidget(self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.addWidget(self.table)

        self.initTable()
        self.setFixedSize(650, 440)

    def initTable(self):
        """ 加载模板数据 """
        dataList = findList()
        self.renderTableData(dataList)

    def renderTableData(self, dataList: list):
        """ 渲染表单数据 """
        self.table.clearContents()
        self.table.setColumnCount(6)
        self.table.setRowCount(len(dataList))
        self.table.setHorizontalHeaderLabels([
            self.tr('ID'), self.tr('编码'), self.tr('模板名称'), self.tr('备注'), self.tr('创建时间'), self.tr('操作')
        ])

        for i, songInfo in enumerate(dataList):
            # 设置行高
            self.table.setRowHeight(i, 51)

            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(str(songInfo[j])))

            cell_widget = QWidget()
            selectButton = PrimaryPushButton(self.tr('查看'), cell_widget)
            selectButton.clicked.connect(lambda state, code=songInfo[1]: self.__onSelectButtonClicked(code))
            layout = QHBoxLayout(cell_widget)
            layout.addWidget(selectButton)
            self.table.setCellWidget(i, 5, cell_widget)

        self.table.resizeColumnsToContents()
        # 设置超过长度后 显示...
        self.table.setColumnWidth(3, 100)
        self.table.setTextElideMode(Qt.ElideRight)

    def __onSelectButtonClicked(self, code: str):
        jsonContent = TemplateContext.getStructure(code)
        w = TextDialogView(title='数据结构', content=jsonContent, parent=self)
        w.exec()


class CodeCardView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QFrame(self)
        self.titleLibraryLabel = StrongBodyLabel(self.tr('模板管理'), self.view)
        self.searchLineEdit = SimpleSearchLineEdit('搜索 模板名称', self.view)
        self.refreshButton = PrimaryPushButton(self.tr('刷新'), self.view)
        self.paperTable = TableFrame(self.view)

        self.contentVBoxLayout = QVBoxLayout(self)
        self.inputHBoxLayout = QHBoxLayout(self)
        self.tableHBoxLayout = QHBoxLayout(self)

        self.contentVBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.contentVBoxLayout.setSpacing(12)
        self.contentVBoxLayout.addWidget(self.titleLibraryLabel, 0, Qt.AlignTop)
        self.contentVBoxLayout.addLayout(self.inputHBoxLayout)
        self.contentVBoxLayout.addLayout(self.tableHBoxLayout)

        self.inputHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.inputHBoxLayout.setSpacing(250)
        self.inputHBoxLayout.addWidget(self.searchLineEdit, 0, Qt.AlignTop)
        self.inputHBoxLayout.addWidget(self.refreshButton, 0, Qt.AlignLeft)

        self.tableHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.tableHBoxLayout.setSpacing(0)
        self.tableHBoxLayout.addWidget(self.paperTable, 0, Qt.AlignLeft)

        self.refreshButton.clicked.connect(self.__onRefreshButtonClicked)
        self.searchLineEdit.clearSignal.connect(self.__onSearchLineClear)
        self.searchLineEdit.searchSignal.connect(self.__onSearchLineSearch)

    def __onSearchLineClear(self):
        self.refreshTable()

    def __onSearchLineSearch(self, keyWord: str):
        dataList = findLikeByName(keyWord)
        self.paperTable.renderTableData(dataList)

    def __onRefreshButtonClicked(self):
        self.paperTable.initTable()

    def refreshTable(self):
        self.paperTable.initTable()


class CodeInterface(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title="数据结构",
            subtitle="在此页面查看模板需要传递的数据结构",
            parent=parent
        )
        self.setObjectName('codeInterface')

        self.codeView = CodeCardView(self)
        self.vBoxLayout.addWidget(self.codeView, 0, Qt.AlignTop)
