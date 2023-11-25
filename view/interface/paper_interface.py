# coding:utf-8
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator

from view.interface.gallery_interface import GalleryInterface
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QTableWidgetItem, QAbstractItemView
from qfluentwidgets import (PrimaryPushButton, StrongBodyLabel, TableWidget, Dialog)
from components.dialog.input_dialog import InputDialogView
from components.frame.frame import SimpleFrame
from components.input.line_edit import SimpleSearchLineEdit

from server.service.paper_service import insert, update, deleteById, findAll, findById, findLikeByName


class PaperInputDialog(InputDialogView):

    def __init__(self, title: str, values: dict = None, parent=None):
        super().__init__(title, parent)
        self.addLineEdit(name=self.tr('纸张名称:'),
                         placeholderText=self.tr('请输入纸张名称'),
                         key='name',
                         value=values['name'] if values and values['name'] else None,
                         validate=QRegExpValidator(QRegExp(".{1,5}"), self))
        self.addSpinBox(name=self.tr('纵向宽度:'),
                        placeholderText=self.tr('请输入纵向宽度'),
                        key='release_width',
                        value=values['release_width'] if values and values['release_width'] else None)
        self.addSpinBox(name=self.tr('纵向高度:'),
                        placeholderText=self.tr('请输入纵向高度'),
                        key='release_height',
                        value=values['release_height'] if values and values['release_height'] else None)
        self.addSpinBox(name=self.tr('横向宽度:'),
                        placeholderText=self.tr('请输入横向宽度'),
                        key='lateral_width',
                        value=values['lateral_width'] if values and values['lateral_width'] else None)
        self.addSpinBox(name=self.tr('横向高度:'),
                        placeholderText=self.tr('请输入横向高度'),
                        key='lateral_height',
                        value=values['lateral_height'] if values and values['lateral_height'] else None)


class TableFrame(SimpleFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = TableWidget(self)
        self.addWidget(self.table)

        self.initTable()
        self.setFixedSize(700, 440)

    def initTable(self):
        """ 加载纸张数据 """
        dataList = findAll()
        self.renderTableData(dataList)

    def renderTableData(self, dataList: list):
        """ 渲染表单数据 """
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.clearContents()
        self.table.setColumnCount(8)
        self.table.setRowCount(len(dataList))
        self.table.setHorizontalHeaderLabels([
            self.tr('ID'), self.tr('纸张名称'), self.tr('纵向宽度'), self.tr('纵向高度'), self.tr('横向宽度'),
            self.tr('横向高度'), self.tr('创建时间'), self.tr('操作')
        ])

        for i, songInfo in enumerate(dataList):
            # 设置行高
            self.table.setRowHeight(i, 51)

            for j in range(7):
                self.table.setItem(i, j, QTableWidgetItem(str(songInfo[j])))

            cell_widget = QWidget()
            updateButton = PrimaryPushButton(self.tr('编辑'), cell_widget)
            deleteButton = PrimaryPushButton(self.tr('删除'), cell_widget)
            updateButton.clicked.connect(lambda state, id=songInfo[0]: self.__onUpdateButtonClicked(id))
            deleteButton.clicked.connect(lambda state, id=songInfo[0]: self.__onDeleteButtonClicked(id))

            layout = QHBoxLayout(cell_widget)
            layout.addWidget(updateButton)
            layout.addWidget(deleteButton)
            self.table.setCellWidget(i, 7, cell_widget)

        self.table.resizeColumnsToContents()
        # 设置超过长度后 显示...
        self.table.setColumnWidth(1, 80)
        self.table.setTextElideMode(Qt.ElideRight)

    def __onUpdateButtonClicked(self, id: str):
        values = findById(id)
        w = PaperInputDialog(title=self.tr('更新'), values=values, parent=self)
        if w.exec():
            data = w.getData()
            data['id'] = id
            update(data=data, parent=self.parent().parent())
            self.initTable()

    def __onDeleteButtonClicked(self, id: str):
        w = Dialog(self.tr('删除'), self.tr('确定删除这条数据吗?此操作不可回滚!'), self)
        w.setTitleBarVisible(False)
        if w.exec():
            deleteById(id)
            self.initTable()


class PaperCardView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QFrame(self)
        self.titleLibraryLabel = StrongBodyLabel(self.tr('纸张管理'), self.view)
        self.searchLineEdit = SimpleSearchLineEdit('搜索 纸张', self.view)
        self.addButton = PrimaryPushButton(self.tr('新增'), self.view)
        self.paperTable = TableFrame(self.view)

        self.contentVBoxLayout = QVBoxLayout(self)
        self.inputHBoxLayout = QHBoxLayout(self)
        self.tableHBoxLayout = QHBoxLayout(self)

        self.__initWidget()

    def __initWidget(self):
        self.contentVBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.contentVBoxLayout.setSpacing(12)
        self.contentVBoxLayout.addWidget(self.titleLibraryLabel, 0, Qt.AlignTop)
        self.contentVBoxLayout.addLayout(self.inputHBoxLayout)
        self.contentVBoxLayout.addLayout(self.tableHBoxLayout)

        self.inputHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.inputHBoxLayout.setSpacing(260)
        self.inputHBoxLayout.addWidget(self.searchLineEdit, 0, Qt.AlignTop)
        self.inputHBoxLayout.addWidget(self.addButton, 0, Qt.AlignLeft)

        self.tableHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.tableHBoxLayout.setSpacing(0)
        self.tableHBoxLayout.addWidget(self.paperTable, 0, Qt.AlignLeft)

        self.addButton.clicked.connect(self.__onAddButtonClicked)
        self.searchLineEdit.clearSignal.connect(self.__onSearchLineClear)
        self.searchLineEdit.searchSignal.connect(self.__onSearchLineSearch)

    def __onAddButtonClicked(self):
        w = PaperInputDialog(title=self.tr('新增'), parent=self)
        if w.exec():
            data = w.getData()
            insert(data=data, parent=self.parent().parent())
            self.paperTable.initTable()

    def __onSearchLineClear(self):
        self.paperTable.initTable()

    def __onSearchLineSearch(self, keyWord: str):
        dataList = findLikeByName(keyWord)
        self.paperTable.renderTableData(dataList)


class PaperInterface(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title='纸张',
            subtitle='设置纸张参数',
            parent=parent
        )
        self.setObjectName('paperInterface')

        self.paperView = PaperCardView(self)
        self.vBoxLayout.addWidget(self.paperView, 0, Qt.AlignTop)
