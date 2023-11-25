# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from view.interface.gallery_interface import GalleryInterface
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QTableWidgetItem, QAbstractItemView
from qfluentwidgets import (PrimaryPushButton, StrongBodyLabel, TableWidget, Dialog)
from components.frame.frame import SimpleFrame
from components.input.line_edit import SimpleSearchLineEdit
from components.custom.template_view import TemplateCardView as TemplateDesignView

from server.service.template_base_service import findList, deleteById, findLikeByName


class TableFrame(SimpleFrame):

    updateChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = TableWidget(self)
        self.addWidget(self.table)

        self.initTable()
        self.setFixedSize(700, 440)

    def initTable(self):
        """ 加载模板数据 """
        dataList = findList()
        self.renderTableData(dataList)

    def renderTableData(self, dataList: list):
        """ 渲染表单数据 """
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
            updateButton = PrimaryPushButton(self.tr('编辑'), cell_widget)
            deleteButton = PrimaryPushButton(self.tr('删除'), cell_widget)
            updateButton.clicked.connect(lambda state, id=songInfo[0]: self.__onUpdateButtonClicked(id))
            deleteButton.clicked.connect(lambda state, id=songInfo[0]: self.__onDeleteButtonClicked(id))

            layout = QHBoxLayout(cell_widget)
            layout.addWidget(updateButton)
            layout.addWidget(deleteButton)
            self.table.setCellWidget(i, 5, cell_widget)

        self.table.resizeColumnsToContents()
        # 设置超过长度后 显示...
        self.table.setColumnWidth(3, 100)
        self.table.setTextElideMode(Qt.ElideRight)

    def __onUpdateButtonClicked(self, id: int):
        self.updateChanged.emit(id)

    def __onDeleteButtonClicked(self, id: int):
        w = Dialog(self.tr('删除'), self.tr('确定删除这条数据吗?此操作不可回滚!'), self)
        w.setTitleBarVisible(False)
        if w.exec():
            deleteById(id)
            self.initTable()


class TemplateCardView(QWidget):

    addButtonChanged = pyqtSignal()
    updButtonChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QFrame(self)
        self.titleLibraryLabel = StrongBodyLabel(self.tr('模板管理'), self.view)
        self.searchLineEdit = SimpleSearchLineEdit('搜索 模板名称', self.view)
        self.addButton = PrimaryPushButton(self.tr('新增'), self.view)
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
        self.inputHBoxLayout.addWidget(self.addButton, 0, Qt.AlignLeft)

        self.tableHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.tableHBoxLayout.setSpacing(0)
        self.tableHBoxLayout.addWidget(self.paperTable, 0, Qt.AlignLeft)

        self.addButton.clicked.connect(self.__onAddButtonClicked)
        self.paperTable.updateChanged.connect(self.__onUpdateChangedClicked)
        self.searchLineEdit.clearSignal.connect(self.__onSearchLineClear)
        self.searchLineEdit.searchSignal.connect(self.__onSearchLineSearch)

    def __onAddButtonClicked(self):
        self.addButtonChanged.emit()

    def __onUpdateChangedClicked(self, id: int):
        self.updButtonChanged.emit(id)

    def __onSearchLineClear(self):
        self.refreshTable()

    def __onSearchLineSearch(self, keyWord: str):
        dataList = findLikeByName(keyWord)
        self.paperTable.renderTableData(dataList)

    def refreshTable(self):
        self.paperTable.initTable()


class TemplateInterFace(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title="模板设计",
            subtitle="在此页面设计您想要的模板吧",
            parent=parent
        )
        self.setObjectName('templateInterface')

        self.templateView = TemplateCardView(self)
        self.templateDesignView = TemplateDesignView(self)
        self.vBoxLayout.addWidget(self.templateView, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.templateDesignView, 0, Qt.AlignTop)

        self.templateDesignView.hide()
        self.__initWidget()

    def __initWidget(self):
        self.templateView.addButtonChanged.connect(self.__onTemplateViewAddButtonChanged)
        self.templateView.updButtonChanged.connect(self.__onTemplateViewUpdButtonChanged)
        self.templateDesignView.returnActionChanged.connect(self.__onTemplateDesignViewReturnActionChanged)

    def __onTemplateViewAddButtonChanged(self):
        self.templateDesignView.initWidget()
        self.templateDesignView.show()
        self.templateView.hide()

    def __onTemplateViewUpdButtonChanged(self, id: int):
        self.templateDesignView.initWidget(id)
        self.templateDesignView.show()
        self.templateView.hide()

    def __onTemplateDesignViewReturnActionChanged(self):
        self.templateView.refreshTable()
        self.templateView.show()
        self.templateDesignView.hide()
