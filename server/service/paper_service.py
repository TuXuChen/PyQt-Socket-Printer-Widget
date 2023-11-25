# coding:utf-8
from PyQt5.QtWidgets import QWidget
from common.message_util import MessageUtil
from server.mapper.paper_mapper import (selectAll, selectById, selectLikeByName, deleteById as delById,
                                        insert as add, update as upd)


def insert(data: dict, parent: QWidget):
    isSuccess = validate(data=data, parent=parent)
    if not isSuccess:
        return
    add(name=data['name'], lateral_width=data['lateral_width'], lateral_height=data['lateral_height'],
        release_width=data['release_width'], release_height=data['release_height'])


def update(data: dict, parent: QWidget):
    isSuccess = validate(data=data, parent=parent)
    if not isSuccess:
        return
    upd(id=data['id'], name=data['name'], lateral_width=data['lateral_width'], lateral_height=data['lateral_height'],
        release_width=data['release_width'], release_height=data['release_height'])


def deleteById(id: str):
    delById(id)


def findById(id: str) -> dict:
    dataList = selectById(id)
    result = {}
    if not dataList:
        return result
    keys = ['id', 'name', 'lateral_width', 'lateral_height', 'release_width', 'release_height', 'create_time']
    data = dataList[0]

    result = {k: v for k, v in zip(keys, data)}
    return result


def findAll() -> list:
    dataList = selectAll()
    return dataList


def findLikeByName(name: str) -> list:
    dataList = selectLikeByName(name)
    return dataList


def findItemAll() -> list:
    dataList = selectAll()
    if not dataList:
        return []
    keys = ['id', 'name', 'lateral_width', 'lateral_height', 'release_width', 'release_height', 'create_time']

    result = [{data[1]: {k: v for k, v in zip(keys, data)}} for data in dataList]
    return result


def validate(data: dict, parent: QWidget) -> bool:
    if data['name'] is None or data['name'] == '':
        MessageUtil.error(parent, '异常信息', '纸张名称不能为空!')
        return False
    return True