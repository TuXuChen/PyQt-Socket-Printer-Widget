# coding:utf-8
import json
from PyQt5.QtCore import Qt, pyqtSignal, QModelIndex
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QTableWidget, QAbstractItemView
from qfluentwidgets import Flyout, InfoBarIcon

from common.table_util import TableUtil
from components.widget.move_widget import TableMoveWidget
from components.widget.from_widget import FromWidget
from common.alignment_util import AlignmentUtil


# 对齐方式
fontAlignmentData = [
    {"左对齐": {"alignment": Qt.AlignVCenter | Qt.AlignLeft}},
    {"居中对齐": {"alignment": Qt.AlignCenter}},
    {"右对齐": {"alignment": Qt.AlignVCenter | Qt.AlignRight}}]

"""
自定义单元格
"""


class TableItem(QTableWidgetItem, QWidget):

    def __init__(self, text: str):
        super().__init__(text)

    def clone_(self, item: QTableWidgetItem):
        text_alignment = self.textAlignment()
        font = self.font()
        foreground = self.foreground()
        item.setFont(font)
        item.setForeground(foreground)
        item.setTextAlignment(text_alignment)

    def widget(self):
        return self


"""
自定义表格
"""


class TableWidget(TableMoveWidget):
    checked = pyqtSignal(QWidget)

    def __init__(self, menuWidget: FromWidget, parent):
        super().__init__(parent)
        margins = parent.contentsMargins()
        self.resize(parent.width() - (margins.right() + margins.left()) - 4, 300)
        self.setColumnCount(1)  # 列数
        self.insertRow(0)
        item = TableItem(self.tr('双击输入文本'))
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setItem(0, 0, item)
        self.setHorizontalHeaderLabels(["number"])
        self.resizeColumnsToContents()
        self.setToolTip(self.tr('1.鼠标放在边框位置可拖动改变表格大小\n2.选中单元格,可设置表格样式'))
        # 上一个选中单元格索引
        self.lastSelectedIndexes = self.selectedIndexes()

        # 菜单
        self.menuWidget = menuWidget
        self.setStyleSheet("gridline-color:rgb(120, 120, 120);")

    def delete(self):
        """ 删除控件 """
        self.menuWidget.delViewLater()
        self.menuWidget.addPromptText("请选中右侧的控件")
        self.deleteLater()

    def rendering(self, data: list):
        """ 渲染控件 """
        renderTable(self, data)

    def getData(self) -> list:
        """ 获取数据结构 """
        dataList = []
        columnCount = self.columnCount()
        rowCount = self.rowCount()
        showGrid = self.showGrid()
        frameShape = False if self.frameShape() != 0 else True
        mergedCells = json.dumps(TableUtil.get_merge_cells_list(self))
        width = self.width()
        height = self.height()
        xCoordinate = self.x()
        yCoordinate = self.y()
        for row in range(rowCount):
            for column in range(columnCount):
                item = self.item(row, column)
                if item:
                    value = item.text()
                    font = item.font()
                    cellAlignment = item.textAlignment()
                    cellWidth = self.columnWidth(item.column())
                    cellHeight = self.rowHeight(item.row())
                    cellFontFamily = font.family()
                    cellFontColor = item.foreground().color().name()
                    cellFontSize = font.pointSize()
                    cellFontItalic = font.italic()
                    cellFontBold = font.bold()
                    cellFontUnderline = font.underline()
                    dataList.append({
                        'columnCount': columnCount,
                        'rowCount': rowCount,
                        'showGrid': showGrid,
                        'frameShape': frameShape,
                        'mergedCells': mergedCells,
                        'row': row,
                        'column': column,
                        'value': value,
                        'cellAlignment': cellAlignment,
                        'cellWidth': cellWidth,
                        'cellHeight': cellHeight,
                        'cellFontFamily': cellFontFamily,
                        'cellFontColor': cellFontColor,
                        'cellFontSize': cellFontSize,
                        'cellFontItalic': cellFontItalic,
                        'cellFontBold': cellFontBold,
                        'cellFontUnderline': cellFontUnderline,
                        'width': width,
                        'height': height,
                        'xCoordinate': xCoordinate,
                        'yCoordinate': yCoordinate
                    })
        return dataList

    def clone_(self, table: QTableWidget):
        """
        克隆
        :param table:
        :return:
        """
        table.verticalHeader().setDefaultSectionSize(30)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)
        table.setStyleSheet(self.styleSheet())
        table.setShowGrid(self.showGrid())  # 隐藏网格线
        table.setFrameShape(self.frameShape())  # 边框
        table.setColumnCount(self.columnCount())
        merged_cells = TableUtil.get_merge_cells(self)
        for row in range(self.rowCount()):
            table.insertRow(row)
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is not None:
                    # 在这里处理单元格内容，item.text() 可以获取单元格文本
                    cell_text = item.text()
                    cell_font = item.font()
                    cell_alignment = item.textAlignment()
                    cell_width = self.columnWidth(item.column())
                    cell_height = self.rowHeight(item.row())
                    cell_item = TableItem(cell_text)
                    cell_item.setFont(cell_font)
                    cell_item.setTextAlignment(cell_alignment)
                    cell_item.setForeground(item.foreground().color())
                    table.setHorizontalHeaderItem(column, TableItem(cell_text))
                    table.setItem(row, column, cell_item)
                    table.setColumnWidth(item.column(), cell_width)
                    table.setRowHeight(item.row(), cell_height)

        # 根据合并单元格信息应用合并单元格策略
        for (row, col), (row_span, col_span) in merged_cells.items():
            table.setSpan(row, col, row_span, col_span)
        table.resize(self.width(), self.height())
        table.move(self.x(), self.y())

    def mousePressEvent(self, evt) -> None:
        """ 鼠标单击事件 """
        if evt.button() == Qt.LeftButton:
            self.checked.emit(self)
            self.initMenuWidget()
        return super().mousePressEvent(evt)

    def getSelectedIndexes(self) -> list[QModelIndex]:
        """  获取选中单元格 """
        itemIndexes = self.selectedIndexes()
        if not itemIndexes:
            itemIndexes = self.lastSelectedIndexes
        else:
            self.lastSelectedIndexes = itemIndexes
        return itemIndexes

    # 获取选中的单元格
    def getSelectedCells(self) -> list:
        selected_items = self.selectedItems()
        selectedCells = [(item.row(), item.column()) for item in selected_items]
        return selectedCells

    def getSelectedWidth(self) -> int:
        """ 获取选中单元格宽度 """
        selectedIndexes = list(self.getSelectedIndexes())
        if selectedIndexes:
            index = selectedIndexes[0]
            col = index.column()
            return self.columnWidth(col)
        return 0

    def getSelectedHeight(self) -> int:
        """ 获取单元格高度 """
        selectedIndexes = list(self.getSelectedIndexes())
        if selectedIndexes:
            index = selectedIndexes[0]
            row = index.row()
            return self.rowHeight(row)
        return 0

    def getSelectedItem(self) -> QTableWidgetItem | None:
        """ 获取选中文本Item """
        selectedIndexes = list(self.getSelectedIndexes())
        if selectedIndexes:
            selected = selectedIndexes[0]
            item = self.item(selected.row(), selected.column())
            return item
        else:
            return None

    def getSelectedAlignment(self) -> int:
        """ 获取对齐方式 """
        item = self.getSelectedItem()
        if item:
            return item.textAlignment()
        else:
            return Qt.AlignVCenter | Qt.AlignLeft

    def getSelectedFont(self) -> QFont:
        """ 获取字体 """
        item = self.getSelectedItem()
        if item:
            return item.font()
        else:
            font = QFont()
            font.setFamily("SimSun")
            font.setPointSize(10)
            font.setItalic(False)
            return font

    def getSelectedFontColor(self) -> QColor:
        """ 获取字体颜色 """
        item = self.getSelectedItem()
        if item:
            return item.foreground().color()
        else:
            return QColor(Qt.black)

    def initMenuWidget(self):
        """ 初始化操作菜单 """
        self.menuWidget.delAll()
        self.menuWidget.addLabelCard(self.tr('基础设置'))
        self.setWidthWidget = self.menuWidget.addSpinBox(self.tr('表格宽度'), self.width(),
                                                         self.__onSetWidthWidgetTextChanged)
        self.setHeightWidget = self.menuWidget.addSpinBox(self.tr('表格高度'), self.height(),
                                                          self.__onSetHeightWidgetTextChanged)
        self.menuWidget.addPushButton(self.tr('新增一列:'),
                                      self.tr('选择'),
                                      self.tr('点击为表格新增一列'),
                                      self.__onAddColumnWidgetClicked)
        self.menuWidget.addPushButton(self.tr('新增一行:'),
                                      self.tr('选择'),
                                      self.tr('点击为表格新增一行'),
                                      self.__onAddRowWidgetClicked)
        self.menuWidget.addPushButton(self.tr('删除一列:'),
                                      self.tr('选择'),
                                      self.tr('点击为表格删除一列'),
                                      self.__onRemoveColumnWidgetClicked)
        self.menuWidget.addPushButton(self.tr('删除一行:'),
                                      self.tr('选择'),
                                      self.tr('点击为表格删除一行'),
                                      self.__onRemoveRowWidgetClicked)
        self.cellWidthWidget = self.menuWidget.addSliderCard(self.tr('单元格宽度:'),
                                                             1, 1000, self.getSelectedWidth(),
                                                             self.__onCellWidthWidgetReleased)
        self.cellHeightWidget = self.menuWidget.addSliderCard(self.tr('单元格宽度:'),
                                                              1, 1000, self.getSelectedHeight(),
                                                              self.__onCellHeightWidgetReleased)
        self.menuWidget.addPushButton(self.tr('合并单元格:'),
                                      self.tr('合并'),
                                      self.tr('点击合并单元格'),
                                      self.__onMergeCellsWidgetClicked)
        self.menuWidget.addSwitchButtonCard(self.tr('显示网格线:'),
                                            self.showGrid(),
                                            self.__onShowGridWidgetClicked)
        self.menuWidget.addSwitchButtonCard(self.tr('显示边框:'),
                                            False if self.frameShape() != 0 else True,
                                            self.__onFrameShapeWidgetClicked)
        self.menuWidget.addLabelCard(self.tr('布局设置'))
        self.menuWidget.addPushButton(self.tr('置于上方:'), self.tr('选泽'), self.tr('点击将控件放置在上方'), lambda: self.raise_())
        self.menuWidget.addPushButton(self.tr('置于下方:'), self.tr('选泽'), self.tr('点击将控件放置在下方'), lambda: self.lower())
        self.menuWidget.addPushButton(self.tr("格式化布局:"),
                                      self.tr('选择'),
                                      self.tr('点击格式化表单布局'),
                                      lambda: self.resizeWidget())
        self.menuWidget.addSwitchButtonCard(self.tr('移动位置:'), self.is_move, self.__onMoveWidgetClicked)
        self.menuWidget.addLabelCard(self.tr('字体设置'))
        self.menuWidget.addFontComboBox(self.tr('字体名称:'),
                                        self.getSelectedFont().family(),
                                        self.__onFontFamilyWidgetClicked)
        self.menuWidget.addColorButtonCard(self.tr('字体颜色:'),
                                           self.getSelectedFontColor().name(),
                                           self.__onFontColorWidgetClicked)
        self.fontSizeWidget = self.menuWidget.addSliderCard(self.tr('字体大小:'), 5, 30,
                                                            self.getSelectedFont().pointSize(),
                                                            self.__onFontSizeWidgetClicked)
        self.menuWidget.addSwitchButtonCard(self.tr('字体斜体:'),
                                            self.getSelectedFont().italic(),
                                            self.__onFontItalicWidgetClicked)
        self.menuWidget.addSwitchButtonCard(self.tr('字体加粗:'),
                                            self.getSelectedFont().bold(),
                                            self.__onFountBoldWidgetClicked)
        self.menuWidget.addSwitchButtonCard(self.tr('字体下划线:'),
                                            self.getSelectedFont().underline(),
                                            self.__onFountUnderlineWidgetClicked)
        self.fontAlignmentWidget = self.menuWidget.addComboBoxCard(self.tr('对齐方式:'),
                                                                   fontAlignmentData,
                                                                   currentText=AlignmentUtil.get_alignment_text(alignment=self.getSelectedAlignment()),
                                                                   callback=self.__onFontAlignmentWidgetClicked)

    def __onSetWidthWidgetTextChanged(self, text):
        text = int(text)
        parent = self.parentWidget()
        max_w = parent.width() - parent.contentsMargins().left() - parent.contentsMargins().right()
        if text > max_w:
            Flyout.create(
                icon=InfoBarIcon.ERROR,
                title='提示信息',
                content=f"表格宽度不能超过{max_w}！",
                target=self.setWidthWidget,
                parent=self,
                isClosable=True
            )
        else:
            self.setFixedWidth(text)

    def __onSetHeightWidgetTextChanged(self, text):
        text = int(text)
        parent = self.parentWidget()
        max_h = parent.height() - parent.contentsMargins().top() - parent.contentsMargins().bottom()
        if text > max_h:
            Flyout.create(
                icon=InfoBarIcon.ERROR,
                title='提示信息',
                content=f"表格高度不能超过{max_h}！",
                target=self.setHeightWidget,
                parent=self,
                isClosable=True
            )
        else:
            self.setFixedHeight(text)

    def __onAddColumnWidgetClicked(self):
        columnName = "Column"
        currentColumnCount = self.columnCount()
        self.setColumnCount(currentColumnCount + 1)
        self.setHorizontalHeaderItem(currentColumnCount, TableItem(columnName))
        for row in range(self.rowCount()):
            item = TableItem("Cell {},{}".format(row + 1, currentColumnCount + 1))
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.setItem(row, currentColumnCount, item)
        self.resizeWidget()

    def __onAddRowWidgetClicked(self):
        currentRowCount = self.rowCount()
        self.insertRow(currentRowCount)
        for row in range(self.columnCount()):
            item = TableItem("Cell {},{}".format(row + 1, currentRowCount + 1))
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.setItem(currentRowCount, row, item)

    def __onRemoveColumnWidgetClicked(self):
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            col = index.column()
            if col != -1:
                self.removeColumn(col)

    def __onRemoveRowWidgetClicked(self):
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            row = index.row()
            if row != -1:
                self.removeRow(row)

    def __onCellWidthWidgetReleased(self):
        width = self.cellWidthWidget.value()
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            col = index.column()
            self.setColumnWidth(col, width)

    def __onCellHeightWidgetReleased(self):
        height = self.cellHeightWidget.value()
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            row = index.row()
            self.setRowHeight(row, height)

    def __onMergeCellsWidgetClicked(self):
        selectedCells = self.getSelectedCells()
        if selectedCells:
            # 排序选中的单元格
            selectedCells.sort()
            start_row, start_col = selectedCells[0]
            end_row, end_col = selectedCells[-1]
            span_rows = end_row - start_row + 1
            span_cols = end_col - start_col + 1
            self.setSpan(start_row, start_col, span_rows, span_cols)

    def __onShowGridWidgetClicked(self, isChecked: bool):
        self.setShowGrid(isChecked)

    def __onFrameShapeWidgetClicked(self, isChecked: bool):
        if isChecked:
            self.setFrameShape(QTableWidget.NoFrame)
        else:
            self.setFrameShape(QTableWidget.StyledPanel)

    def __onMoveWidgetClicked(self, isChecked: bool):
        self.is_move = isChecked

    def __onFontFamilyWidgetClicked(self, family: str):
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            item = self.item(index.row(), index.column())
            if not item:
                continue
            font = item.font()
            font.setFamily(family)
            item.setFont(font)

    def __onFontColorWidgetClicked(self, color: QColor):
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            item = self.item(index.row(), index.column())
            if item:
                item.setForeground(color)

    def __onFontSizeWidgetClicked(self):
        size = self.fontSizeWidget.value()
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            item = self.item(index.row(), index.column())
            if not item:
                continue
            font = item.font()
            font.setPointSize(size)
            item.setFont(font)

    def __onFontItalicWidgetClicked(self, isChecked: bool):
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            item = self.item(index.row(), index.column())
            if not item:
                continue
            font = item.font()
            font.setItalic(isChecked)
            item.setFont(font)

    def __onFountUnderlineWidgetClicked(self, isChecked: bool):
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            item = self.item(index.row(), index.column())
            if not item:
                continue
            font = item.font()
            font.setUnderline(isChecked)
            item.setFont(font)

    def __onFountBoldWidgetClicked(self, isChecked: bool):
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            item = self.item(index.row(), index.column())
            if not item:
                continue
            font = item.font()
            font.setBold(isChecked)
            item.setFont(font)

    def __onFontAlignmentWidgetClicked(self):
        alignment = self.fontAlignmentWidget.currentData()["alignment"]
        selectedIndexes = self.getSelectedIndexes()
        for index in selectedIndexes:
            self.item(index.row(), index.column()).setTextAlignment(alignment)


def renderTable(widget: QTableWidget, data: list):
    """ 渲染表格控件 """
    tableDict = data[0]
    widget.setShowGrid(False if tableDict['show_grid'] == 0 else True)
    widget.setColumnCount(tableDict['column_count'])
    widget.setRowCount(tableDict['row_count'])
    if tableDict['frame_shape'] == 0:
        widget.setFrameShape(QTableWidget.StyledPanel)
    else:
        widget.setFrameShape(QTableWidget.NoFrame)
    for dbTable in data:
        row = dbTable['row']
        column = dbTable['column']
        item = TableItem(dbTable['value'])
        item.setTextAlignment(dbTable['cell_alignment'])
        font = item.font()
        font.setFamily(dbTable['cell_font_family'])
        font.setItalic(False if dbTable['cell_font_italic'] == 0 else True)
        font.setPointSize(dbTable['cell_font_size'])
        font.setBold(False if dbTable['cell_font_bold'] == 0 else True)
        font.setUnderline(False if dbTable['cell_font_underline'] == 0 else True)
        item.setFont(font)
        item.setForeground(QColor(dbTable['cell_font_color']))
        widget.setItem(row, column, item)
        widget.setColumnWidth(column, dbTable['cell_width'])
        widget.setRowHeight(row, dbTable['cell_height'])

    mergedCells = json.loads(tableDict['merged_cells'])
    if mergedCells:
        for merged in mergedCells:
            widget.setSpan(merged[0], merged[1], merged[2], merged[3])
    widget.resize(tableDict['width'], tableDict['height'])
    widget.move(tableDict['x_coordinate'], tableDict['y_coordinate'])
