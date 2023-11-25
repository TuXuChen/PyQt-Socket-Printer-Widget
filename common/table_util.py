# coding: utf-8
from PyQt5.QtWidgets import QTableWidget


class TableUtil:

    @staticmethod
    def get_merge_cells(table: QTableWidget):
        merged_cells = {}  # 创建一个空字典用于存储合并单元格信息
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item is not None:
                    row_span = table.rowSpan(row, col)
                    col_span = table.columnSpan(row, col)
                    if row_span > 1 or col_span > 1:
                        print(f"Cell at ({row}, {col}) is spanned with row span {row_span} and column span {col_span}")
                        # 将合并单元格信息添加到字典中
                        merged_cells[(row, col)] = (row_span, col_span)
        return merged_cells

    @staticmethod
    def get_merge_cells_list(table: QTableWidget):
        data = []
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item is not None:
                    row_span = table.rowSpan(row, col)
                    col_span = table.columnSpan(row, col)
                    if row_span > 1 or col_span > 1:
                        print(f"Cell at ({row}, {col}) is spanned with row span {row_span} and column span {col_span}")
                        data.append((row, col, row_span, col_span,))
        return data