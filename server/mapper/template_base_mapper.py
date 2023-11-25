# coding:utf-8
from server.config.sqlite_config import sql_execute

"""
模板基础
"""


def insert(code: str, name: str, remark: str, paperName: str, direction: str, paperWidth: int,
           paperHeight: int, leftMargin: int, rightMargin: int, topMargin: int, bottomMargin: int,
           backgroundImage: str = None):
    """
    新增
    :param code 编码
    :param name 模板名称
    :param remark: 备注
    :param paperName: 纸张名称
    :param direction: 打印方向
    :param paperWidth: 宽
    :param paperHeight: 高
    :param leftMargin: 左
    :param rightMargin: 右
    :param topMargin: 上
    :param bottomMargin: 下
    :param backgroundImage: 背景
    :return:
    """
    sql = """
    insert into t_printer_template_base (code, name, remark, paper_name, direction, paper_width,
    paper_height, left_margin, right_margin, top_margin, bottom_margin, background_image, create_time)
    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """
    values = (code, name, remark, paperName, direction, paperWidth, paperHeight, leftMargin, rightMargin, topMargin, bottomMargin,
              backgroundImage,)
    sql_execute.execute(sql, values)


def update(id: int, name: str, remark: str, paperName: str, direction: str, paperWidth: int,
           paperHeight: int, leftMargin: int, rightMargin: int, topMargin: int, bottomMargin: int,
           backgroundImage: str = None):
    sql = """
    update t_printer_template_base set name=?, remark=?, paper_name=?, direction=?, paper_width=?,
    paper_height=?, left_margin=?, right_margin=?, top_margin=?, bottom_margin=?, background_image=? where id = ?
    """
    values = (name, remark, paperName, direction, paperWidth, paperHeight, leftMargin, rightMargin, topMargin, bottomMargin, backgroundImage, id,)
    sql_execute.execute(sql, values)


def deleteById(id: int):
    sql = """ delete from t_printer_template_base where id = ?"""
    values = (id,)
    sql_execute.execute(sql, values)


def selectById(id: int) -> list:
    sql = f"""select id, code, name, remark, paper_name, direction, paper_width,
    paper_height, left_margin, right_margin, top_margin, bottom_margin, background_image, create_time from t_printer_template_base
    where id = {id}"""
    return sql_execute.execute_query(sql)


def selectByCode(code: str) -> list:
    sql = f"""select id, code, name, remark, paper_name, direction, paper_width,
        paper_height, left_margin, right_margin, top_margin, bottom_margin, background_image, create_time from t_printer_template_base
        where code = '{code}'"""
    return sql_execute.execute_query(sql)

def selectAll() -> list:
    sql = """
    select id, code, name, remark, paper_name, direction, paper_width,
    paper_height, left_margin, right_margin, top_margin, bottom_margin, background_image, create_time from t_printer_template_base
    """
    return sql_execute.execute_query(sql)


def selectList() -> list:
    sql = """
    select id, code, name, remark, create_time from t_printer_template_base order by create_time desc
    """
    return sql_execute.execute_query(sql)


def selectLikeByName(name: str) -> list:
    sql = f""" select id, code, name, remark, create_time from t_printer_template_base where name like '%{name}%'"""
    return sql_execute.execute_query(sql)
