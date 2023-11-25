# coding:utf-8
import os
import sqlite3
from dbutils.persistent_db import PersistentDB


class SQLiteConfiguration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_connection()
        return cls._instance

    def init_connection(self):
        # 获取数据库文件的绝对路径
        current_dir = os.path.dirname(__file__)
        db_file_path = os.path.abspath(os.path.join(current_dir, f"../../resource/printer_database.db"))
        pyinstallerDbPath = r'./db/printer_database.db'
        self.pool = PersistentDB(sqlite3, maxusage=2, database=db_file_path)

    def get_connection(self):
        return self.pool.connection()

    def execute_query(self, sql: str) -> any:
        connection = self.pool.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()
        return result

    def execute(self, sql: str, values: any = None):
        connection = self.pool.connection()
        cursor = connection.cursor()
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        connection.commit()
        connection.close()

    def commit(self):
        """ 提交事务 """
        connection = self.pool.connection()
        connection.commit()

    def rollback(self):
        """ 回滚事务 """
        connection = self.pool.connection()
        connection.rollback()

    def close(self):
        connection = self.pool.connection()
        connection.close()


sql_execute = SQLiteConfiguration()
