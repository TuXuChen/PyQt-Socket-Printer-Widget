# coding:utf-8
from server.config.sqlite_config import sql_execute

"""
模板单行文本基础
"""


def insert(templateCode: str, value: str, printerType: int, border: int, borderSize: int, borderType: int, width: int, height: int,
           xCoordinate: int, yCoordinate: int, fontSize: int, fontFamily: str, fontColor: str, fontItalic: bool, fontBold: bool,
           fontUnderline: bool, fontAlignment: int):
    """
    单行文本
    :param templateCode:
    :param value:
    :param printerType:
    :param border:
    :param borderSize:
    :param borderType:
    :param width:
    :param height:
    :param xCoordinate:
    :param yCoordinate:
    :param fontSize:
    :param fontFamily:
    :param fontColor:
    :param fontItalic:
    :param fontBold:
    :param fontUnderline:
    :param fontAlignment:
    :return:
    """
    sql = """
    insert into t_printer_template_label (template_code, value, printer_type, border, border_size, border_type, width, height,
    x_coordinate, y_coordinate, font_size, font_family, font_color, font_italic, font_bold, font_underline, font_alignment) values 
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    values = (templateCode, value, printerType, border, borderSize, borderType, width, height,
              xCoordinate, yCoordinate, fontSize, fontFamily, fontColor, fontItalic, fontBold,
              fontUnderline, fontAlignment,)
    sql_execute.execute(sql, values)


def deleteByTemplateCode(templateCode: str):
    sql = """delete from t_printer_template_label where template_code = ?"""
    values = (templateCode,)
    sql_execute.execute(sql, values)


def selectByTemplateCode(templateCode: str) -> list:
    sql = f"""select id, template_code, value, printer_type, border, border_size, border_type, width, height,
    x_coordinate, y_coordinate, font_size, font_family, font_color, font_italic, font_bold, font_underline, font_alignment from t_printer_template_label
    where template_code = '{templateCode}' """
    return sql_execute.execute_query(sql)
