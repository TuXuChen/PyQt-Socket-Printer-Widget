# coding:utf-8
from server.config.sqlite_config import sql_execute

"""
表格控件
"""


def insert(templateCode: str, columnCount: int, rowCount: int, showGrid: bool, frameShape: bool,
           mergedCells: str, row: int, column: int, value: str, cellAlignment: int, cellWidth: int,
           cellHeight: int, cellFontFamily: str, cellFontColor: str, cellFontSize: int, cellFontItalic: bool,
           cellFontBold: bool, cellFontUnderline: bool, width: int, height: int, xCoordinate: int, yCoordinate: int):
    """
    新增
    :param templateCode:
    :param columnCount:
    :param rowCount:
    :param showGrid:
    :param frameShape:
    :param mergedCells:
    :param row:
    :param column:
    :param value:
    :param cellAlignment:
    :param cellWidth:
    :param cellHeight:
    :param cellFontFamily:
    :param cellFontColor:
    :param cellFontSize:
    :param cellFontItalic:
    :param cellFontBold:
    :param cellFontUnderline:
    :param width:
    :param height:
    :param xCoordinate:
    :param yCoordinate:
    :return:
    """
    sql = """
    insert into t_printer_template_table (template_code, column_count, row_count, show_grid, frame_shape, merged_cells,
    row, column, value, cell_alignment, cell_width, cell_height, cell_font_family, cell_font_color, cell_font_size, cell_font_italic,
    cell_font_bold, cell_font_underline, width, height, x_coordinate, y_coordinate) values (
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    values = (templateCode, columnCount, rowCount, showGrid, frameShape,
              mergedCells, row, column, value, cellAlignment, cellWidth,
              cellHeight, cellFontFamily, cellFontColor, cellFontSize, cellFontItalic,
              cellFontBold, cellFontUnderline, width, height, xCoordinate, yCoordinate,)
    sql_execute.execute(sql, values)


def deleteByTemplateCode(templateCode: str):
    sql = """delete from t_printer_template_table where template_code = ?"""
    values = (templateCode,)
    sql_execute.execute(sql, values)


def selectByTemplateCode(templateCode: str) -> list:
    sql = f"""select id, template_code, value, column_count, row_count, show_grid, frame_shape, merged_cells,
    row, column, cell_alignment, cell_width, cell_height, cell_font_family, cell_font_color, cell_font_size, cell_font_italic,
    cell_font_bold, cell_font_underline, width, height, x_coordinate, y_coordinate from t_printer_template_table
    where template_code = '{templateCode}' order by row,column asc"""
    return sql_execute.execute_query(sql)
