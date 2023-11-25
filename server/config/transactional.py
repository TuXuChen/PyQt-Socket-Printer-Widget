# coding:utf-8
import threading
from server.config.sqlite_config import sql_execute

""" 事务 """


def transactional():
    requests_lock = threading.Lock()

    def decorator(func):
        def wrapper(*args, **kwargs):
            with requests_lock:
                try:
                    result = func(*args, **kwargs)
                    sql_execute.commit()
                    return result
                except Exception as e:
                    sql_execute.rollback()
                    raise
                finally:
                    sql_execute.close()

        return wrapper

    return decorator
