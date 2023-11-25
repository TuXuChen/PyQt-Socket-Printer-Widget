# coding:utf-8
from server.config.sqlite_config import sql_execute

"""
图片控件
"""


def insert(templateCode: str, value: str, printerType: int, width: int, height: int,
           opacity: float, xCoordinate: int, yCoordinate: int):
    """
    新增
    :param templateCode:
    :param value:
    :param printerType:
    :param width:
    :param height:
    :param opacity:
    :param xCoordinate:
    :param yCoordinate:
    :return:
    """
    sql = """
    insert into t_printer_template_image (template_code, value, printer_type, width, height, opacity,
    x_coordinate, y_coordinate) values (?,?,?,?,?,?,?,?)
    """
    values = (templateCode, value, printerType, width, height, opacity, xCoordinate, yCoordinate,)
    sql_execute.execute(sql, values)


def deleteByTemplateCode(templateCode: str):
    sql = """delete from t_printer_template_image where template_code = ?"""
    values = (templateCode,)
    sql_execute.execute(sql, values)


def selectByTemplateCode(templateCode: str) -> list:
    sql = f""" select id, template_code, value, printer_type, width, height, opacity,
    x_coordinate, y_coordinate from t_printer_template_image where template_code = '{templateCode}' """
    return sql_execute.execute_query(sql)
