# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget
from common.cursor_util import CursorUtil

'''
自定义可移动的窗口
'''


class SimpleMoveQWidget(QWidget):

    def mousePressEvent(self, evt):
        # 鼠标左键时运行
        if evt.buttons() == Qt.LeftButton:
            # 是否移动
            self.is_move = True
            self.window_x = self.x()
            self.window_y = self.y()
            self.mouse_x = evt.globalX()
            self.mouse_y = evt.globalY()

    def mouseMoveEvent(self, evt):
        if self.is_move is not None and self.is_move:
            # 坐标原点 加上向量
            x = self.window_x + (evt.globalX() - self.mouse_x)
            y = self.window_y + (evt.globalY() - self.mouse_y)
            # 获取当前窗口的父级（通常是主窗口）
            parent_widget = self.parentWidget()
            if parent_widget is not None:
                margins = parent_widget.contentsMargins()
                parent_contents_rect = parent_widget.contentsRect()
                parent_width = parent_contents_rect.width()
                parent_height = parent_contents_rect.height()
                parent_left_margin = margins.left()
                parent_top_margin = margins.top()
                parent_right_margin = parent_widget.width() - parent_width - margins.right()
                parent_bottom_margin = parent_widget.height() - parent_height - margins.bottom()
                # 在这里稍微调整右边和下边的限制
                if margins.left() != margins.right():
                    x = max(parent_left_margin, min(x, parent_width - self.width() - parent_right_margin + (
                            margins.left() + margins.right()) - 20))
                else:
                    x = max(parent_left_margin, min(x, parent_width - self.width() - parent_right_margin + (
                            margins.left() + margins.right())))

                if margins.top() != margins.bottom():
                    y = max(parent_top_margin, min(y, parent_height - self.height() - parent_bottom_margin + (
                            margins.top() + margins.bottom()) - 20))
                else:
                    y = max(parent_top_margin, min(y, parent_height - self.height() - parent_bottom_margin + (
                            margins.top() + margins.bottom())))

            else:
                parent_width = QApplication.desktop().width()
                parent_height = QApplication.desktop().height()
                x = max(0, min(x, parent_width - self.width()))
                y = max(0, min(y, parent_height - self.height()))
            # 确保窗口移动范围在父级限制内
            # 移动窗口
            self.move(x, y)

    def mouseReleaseEvent(self, evt):
        self.is_move = False


'''
自定义可移动 边框可拖拽改变大小的窗口
'''


class MoveSizeQWidget(QWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.is_centre_move = False
        self.is_left_move = False
        self.is_right_move = False
        self.is_top_move = False
        self.is_bottom_move = False
        self.min_width = 30
        self.min_height = 20

    def enterEvent(self, evt) -> None:
        # 获取鼠标相对于控件的位置
        mouse_pos = evt.pos()
        width = self.width()
        height = self.height()
        # 判断鼠标位置是否在边界
        on_left_edge = mouse_pos.x() <= 2
        on_right_edge = mouse_pos.x() >= width - 2
        on_top_edge = mouse_pos.y() <= 1
        on_bottom_edge = mouse_pos.y() >= height - 1
        if on_left_edge or on_right_edge:
            # 设置左右箭头形状
            self.setCursor(Qt.SizeHorCursor)
        elif on_top_edge or on_bottom_edge:
            # 设置上下箭头形状
            self.setCursor(Qt.SizeVerCursor)
        else:
            # 设置小手形状
            self.setCursor(Qt.PointingHandCursor)
        return super().enterEvent(evt)

    def leaveEvent(self, event):
        # 当鼠标离开控件时触发
        self.unsetCursor()
        return super().leaveEvent(event)

    def mousePressEvent(self, evt) -> None:
        # 鼠标左键时运行
        if evt.buttons() != Qt.LeftButton:
            return super().mousePressEvent(evt)
        mouse_pos = evt.pos()
        width = self.width()
        height = self.height()
        # 判断鼠标位置是否在边界
        on_left_edge = mouse_pos.x() <= 3
        on_right_edge = mouse_pos.x() >= width - 3
        on_top_edge = mouse_pos.y() <= 3
        on_bottom_edge = mouse_pos.y() >= height - 3
        if on_left_edge:
            self.is_left_move = True
        elif on_right_edge:
            self.is_right_move = True
        elif on_top_edge:
            self.is_top_move = True
        elif on_bottom_edge:
            self.is_bottom_move = True
        else:
            # 是否移动
            self.is_centre_move = True
        self.window_x = self.x()
        self.window_y = self.y()
        self.mouse_x = evt.globalX()
        self.mouse_y = evt.globalY()
        self.mouse_pos = evt.pos()
        self.mouse_width = self.width()
        self.mouse_height = self.height()
        return super().mousePressEvent(evt)

    def mouseMoveEvent(self, evt) -> None:
        # 　计算向量
        now_x = evt.globalX() - self.mouse_x
        now_y = evt.globalY() - self.mouse_y
        # 坐标原点 加上向量
        x = self.window_x + now_x
        y = self.window_y + now_y
        # 左移动 改变窗口尺寸
        delta = evt.pos() - self.mouse_pos
        # 移动窗口
        if self.is_centre_move:
            # 获取当前窗口的父级（通常是主窗口）
            parent_widget = self.parentWidget()
            if parent_widget is not None:
                margins = parent_widget.contentsMargins()
                parent_contents_rect = parent_widget.contentsRect()
                parent_width = parent_contents_rect.width()
                parent_height = parent_contents_rect.height()
                parent_left_margin = margins.left()
                parent_top_margin = margins.top()
                parent_right_margin = parent_widget.width() - parent_width - margins.right()
                parent_bottom_margin = parent_widget.height() - parent_height - margins.bottom()
                # 在这里稍微调整右边和下边的限制
                if margins.left() != margins.right():
                    x = max(parent_left_margin, min(x, parent_width - self.width() - parent_right_margin + (
                            margins.left() + margins.right()) - 20))
                else:
                    x = max(parent_left_margin, min(x, parent_width - self.width() - parent_right_margin + (
                            margins.left() + margins.right())))

                if margins.top() != margins.bottom():
                    y = max(parent_top_margin, min(y, parent_height - self.height() - parent_bottom_margin + (
                            margins.top() + margins.bottom()) - 20))
                else:
                    y = max(parent_top_margin, min(y, parent_height - self.height() - parent_bottom_margin + (
                            margins.top() + margins.bottom())))

            else:
                parent_width = QApplication.desktop().width()
                parent_height = QApplication.desktop().height()
                x = max(0, min(x, parent_width - self.width()))
                y = max(0, min(y, parent_height - self.height()))
            # 确保窗口移动范围在父级限制内
            # 移动窗口
            self.move(x, y)
        elif self.is_left_move:
            new_width = self.size().width() - delta.x()
            new_width = self.min_width if new_width < self.min_width else new_width
            x = self.window_x + now_x  # 调整x坐标
            self.resize(new_width, self.height())
            self.move(x, self.window_y)  # 移动窗口
        elif self.is_right_move:
            new_width = self.mouse_width + now_x
            new_width = self.min_width if new_width < self.min_width else new_width
            self.resize(new_width, self.height())
        elif self.is_top_move:
            new_height = self.size().height() - delta.y()
            new_height = self.min_height if new_height < self.min_height else new_height
            y = self.window_y + now_y
            self.resize(self.size().width(), new_height)
            self.move(self.window_x, y)
        elif self.is_bottom_move:
            new_height = self.mouse_height + now_y
            new_height = self.min_height if new_height < self.min_height else new_height
            self.resize(self.size().width(), new_height)
        return super().mouseMoveEvent(evt)

    def mouseReleaseEvent(self, evt) -> None:
        self.is_centre_move = False
        self.is_left_move = False
        self.is_right_move = False
        self.is_top_move = False
        self.is_bottom_move = False
        return super().mouseReleaseEvent(evt)


"""
边框可拖动的QTable
"""


class TableMoveWidget(QTableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.verticalHeader().setDefaultSectionSize(30)  # 设置行高
        self.setEditTriggers(QTableWidget.DoubleClicked)
        self.setSelectionBehavior(QTableWidget.SelectItems)
        self.setDragDropMode(QTableWidget.InternalMove)
        self.setShowGrid(True)  # 隐藏网格线
        self.setDragDropOverwriteMode(False)  # 需要设置为 False
        self.setDragEnabled(False)  # 文本拖动
        self.setMouseTracking(False)  # 鼠标移动
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        # 移动窗口
        self.is_move = False
        # self.is_centre_move = False
        # self.is_left_move = False
        # self.is_right_move = False
        # self.is_top_move = False
        # self.is_bottom_move = False
        # self.min_width = 30
        # self.min_height = 20
    #
    # # 鼠标进入控件事件
    # def enterEvent(self, evt) -> None:
    #     mouse_pos = evt.pos()
    #     CursorUtil.cursor_style(self, mouse_pos)
    #     return super().enterEvent(evt)
    #
    # # 鼠标离开控件事件
    # def leaveEvent(self, event):
    #     # 当鼠标离开控件时触发
    #     self.unsetCursor()
    #     return super().leaveEvent(event)
    #
    # # 左键单击事件
    # def mousePressEvent(self, event) -> None:
    #     if event.buttons() != Qt.LeftButton:
    #         return super().mousePressEvent(event)
    #     mouse_pos = event.pos()
    #     width = self.width()
    #     height = self.height()
    #     # 判断鼠标位置是否在边界
    #     on_left_edge = mouse_pos.x() <= 3
    #     on_right_edge = mouse_pos.x() >= width - 3
    #     on_top_edge = mouse_pos.y() <= 3
    #     on_bottom_edge = mouse_pos.y() >= height - 3
    #     if on_left_edge:
    #         self.is_left_move = True
    #     elif on_right_edge:
    #         self.is_right_move = True
    #     elif on_top_edge:
    #         self.is_top_move = True
    #     elif on_bottom_edge:
    #         self.is_bottom_move = True
    #     else:
    #         index = self.indexAt(event.pos())
    #         if index.isValid():
    #             self.clearSelection()
    #             self.setCurrentCell(index.row(), index.column())
    #             self.drag_start_pos = event.pos()
    #     self.window_x = self.x()
    #     self.window_y = self.y()
    #     self.mouse_x = event.globalX()
    #     self.mouse_y = event.globalY()
    #     self.mouse_pos = event.pos()
    #     self.mouse_width = self.width()
    #     self.mouse_height = self.height()
    #     return super().mousePressEvent(event)
    #
    # # 鼠标移动事件
    # def mouseMoveEvent(self, event) -> None:
    #     global max_width
    #     CursorUtil.cursor_style(self, event.pos())
    #     # 获取当前窗口的父级（通常是主窗口）
    #     parent_widget = self.parentWidget()
    #     if parent_widget is not None:
    #         margins = parent_widget.contentsMargins()
    #         max_width = parent_widget.width() - margins.right() - margins.left() - 4
    #     if self.is_left_move:
    #         delta = event.pos() - self.mouse_pos
    #         now_x = event.globalX() - self.mouse_x
    #         new_width = self.size().width() - delta.x()
    #         new_width = self.min_width if new_width < self.min_width else new_width
    #         x = self.window_x + now_x  # 调整x坐标
    #         if max_width is not None and parent_widget is not None:
    #             new_width = max_width if max_width < new_width else new_width
    #             x = parent_widget.contentsMargins().left() + 2 if x < parent_widget.contentsMargins().left() else x
    #         self.resize(new_width, self.height())
    #         self.move(x, self.window_y)  # 移动窗口
    #     elif self.is_right_move:
    #         now_x = event.globalX() - self.mouse_x
    #         new_width = self.mouse_width + now_x
    #         new_width = self.min_width if new_width < self.min_width else new_width
    #         if max_width is not None and parent_widget is not None:
    #             new_width = max_width if max_width < new_width else new_width
    #         self.resize(new_width, self.height())
    #     elif self.is_top_move:
    #         delta = event.pos() - self.mouse_pos
    #         now_y = event.globalY() - self.mouse_y
    #         new_height = self.size().height() - delta.y()
    #         new_height = self.min_height if new_height < self.min_height else new_height
    #         y = self.window_y + now_y
    #         self.resize(self.size().width(), new_height)
    #         self.move(self.window_x, y)
    #     elif self.is_bottom_move:
    #         now_y = event.globalY() - self.mouse_y
    #         new_height = self.mouse_height + now_y
    #         new_height = self.min_height if new_height < self.min_height else new_height
    #         self.resize(self.size().width(), new_height)
    #     elif hasattr(self, 'drag_start_pos'):
    #         drag_distance = (event.pos() - self.drag_start_pos).manhattanLength()
    #         if drag_distance >= QApplication.startDragDistance():
    #             self.clearSelection()
    #             top_left_item = self.itemAt(self.drag_start_pos)
    #             bottom_right_item = self.itemAt(event.pos())
    #             if top_left_item and bottom_right_item:
    #                 top_left_row = top_left_item.row()
    #                 bottom_right_row = bottom_right_item.row()
    #                 top_left_col = top_left_item.column()
    #                 bottom_right_col = bottom_right_item.column()
    #                 for row in range(top_left_row, bottom_right_row + 1):
    #                     for col in range(top_left_col, bottom_right_col + 1):
    #                         self.item(row, col).setSelected(True)
    #
    #     return super().mouseMoveEvent(event)
    #
    # # 鼠标释放事件
    # def mouseReleaseEvent(self, event) -> None:
    #     self.is_left_move = False
    #     self.is_right_move = False
    #     self.is_top_move = False
    #     self.is_bottom_move = False
    #     if hasattr(self, 'drag_start_pos'):
    #         del self.drag_start_pos
    #     return super().mouseReleaseEvent(event)

    def mousePressEvent(self, evt):
        # 鼠标左键时运行
        if evt.buttons() == Qt.LeftButton and self.is_move:
            self.window_x = self.x()
            self.window_y = self.y()
            self.mouse_x = evt.globalX()
            self.mouse_y = evt.globalY()
        else:
            return super().mousePressEvent(evt)

    def mouseMoveEvent(self, evt):
        if self.is_move:
            # 坐标原点 加上向量
            x = self.window_x + (evt.globalX() - self.mouse_x)
            y = self.window_y + (evt.globalY() - self.mouse_y)
            # 获取当前窗口的父级（通常是主窗口）
            parent_widget = self.parentWidget()
            if parent_widget is not None:
                margins = parent_widget.contentsMargins()
                parent_contents_rect = parent_widget.contentsRect()
                parent_width = parent_contents_rect.width()
                parent_height = parent_contents_rect.height()
                parent_left_margin = margins.left()
                parent_top_margin = margins.top()
                parent_right_margin = parent_widget.width() - parent_width - margins.right()
                parent_bottom_margin = parent_widget.height() - parent_height - margins.bottom()
                # 在这里稍微调整右边和下边的限制
                if margins.left() != margins.right():
                    x = max(parent_left_margin, min(x, parent_width - self.width() - parent_right_margin + (
                            margins.left() + margins.right()) - 20))
                else:
                    x = max(parent_left_margin, min(x, parent_width - self.width() - parent_right_margin + (
                            margins.left() + margins.right())))

                if margins.top() != margins.bottom():
                    y = max(parent_top_margin, min(y, parent_height - self.height() - parent_bottom_margin + (
                            margins.top() + margins.bottom()) - 20))
                else:
                    y = max(parent_top_margin, min(y, parent_height - self.height() - parent_bottom_margin + (
                            margins.top() + margins.bottom())))

            else:
                parent_width = QApplication.desktop().width()
                parent_height = QApplication.desktop().height()
                x = max(0, min(x, parent_width - self.width()))
                y = max(0, min(y, parent_height - self.height()))
            # 确保窗口移动范围在父级限制内
            # 移动窗口
            self.move(x, y)
        else:
            return super().mouseMoveEvent(evt)

    # 窗口改变事件
    def resizeEvent(self, event) -> None:
        self.resizeWidget()
        return super().resizeEvent(event)

    # 设置每列宽度一样
    def resizeWidget(self):
        width = self.width()
        width = width - (self.contentsMargins().right() + self.contentsMargins().left()) + 5
        num_columns = self.model().columnCount()
        column_width = width // num_columns if num_columns > 0 else width
        for col in range(num_columns):
            self.setColumnWidth(col, int(column_width))

        height = self.height()
        height = height - (self.contentsMargins().top() + self.contentsMargins().bottom())
        total_height = 0
        num_rows = self.model().rowCount()
        for row in range(num_rows):
            row_height = self.rowHeight(row)
            total_height += row_height
        if total_height >= height:
            self.setFixedHeight(total_height + 2)
