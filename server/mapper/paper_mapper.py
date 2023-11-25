# coding:utf-8
from server.config.sqlite_config import sql_execute

"""
纸张数据
"""


def insert(name: str, lateral_width: int, lateral_height: int,
           release_width: int, release_height: int):
    sql = """
    insert into t_printer_paper (name, lateral_width, lateral_height, release_width, release_height, create_time) values
    (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """
    values = (name, lateral_width, lateral_height, release_width, release_height,)
    sql_execute.execute(sql, values)


def update(id: int, name: str, lateral_width: int, lateral_height: int,
           release_width: int, release_height: int):
    sql = """
    update t_printer_paper set name=?, lateral_width=?, lateral_height=?, release_width=?, release_height=? where id = ?
    """
    values = (name, lateral_width, lateral_height, release_width, release_height, id,)
    sql_execute.execute(sql, values)


def deleteById(id: str):
    sql = """delete from t_printer_paper where id = ?"""
    values = (id,)
    sql_execute.execute(sql, values)


def selectById(id: str) -> list:
    sql = f"""select id, name, lateral_width, lateral_height, release_width, release_height, create_time from t_printer_paper where id = {id}"""
    return sql_execute.execute_query(sql)


def selectAll() -> list:
    sql = """select id, name, lateral_width, lateral_height, release_width, release_height, create_time from t_printer_paper order by id asc"""
    return sql_execute.execute_query(sql)


def selectLikeByName(name: str) -> list:
    sql = f"""select id, name, lateral_width, lateral_height, release_width, release_height, create_time from t_printer_paper where name like '%{name}%'"""
    return sql_execute.execute_query(sql)
