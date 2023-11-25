# coding:utf-8
from PyQt5.QtWidgets import QWidget
from common.message_util import MessageUtil
from server.mapper.template_base_mapper import (insert as add, update as upd, deleteById as delById,
                                                selectAll, selectById, selectLikeByName, selectList, selectByCode)

from common.random_util import getCode
from server.service.template_label_service import (insert as labelInsert, deleteByTemplateCode as labelDelByTemplate)
from server.service.template_image_service import (insert as imageInsert, deleteByTemplateCode as imageDelByTemplate)
from server.service.template_table_service import (insert as tableInsert, deleteByTemplateCode as tableDelByTemplate)


def save(data: dict, parent: QWidget):
    paperInfo = data['paperInfo']
    isSuccess = validate(data=paperInfo, parent=parent)
    if not isSuccess:
        return
    if not paperInfo['id']:
        code = insert(paperInfo)
    else:
        code = update(paperInfo)
        labelDelByTemplate(code)
        imageDelByTemplate(code)
        tableDelByTemplate(code)
    if data['labelList']:
        for label in data['labelList']:
            label['templateCode'] = code
            labelInsert(label)
    if data['imageList']:
        for image in data['imageList']:
            image['templateCode'] = code
            imageInsert(image)
    if data['tableList']:
        for table in data['tableList']:
            table['templateCode'] = code
            tableInsert(table)


def insert(data: dict) -> str:
    code = getCode()
    add(code=code, name=data['name'], remark=data['remark'], paperName=data['paperName'], direction=data['direction'],
        paperWidth=data['paperWidth'], paperHeight=data['paperHeight'], leftMargin=data['leftMargin'],
        topMargin=data['topMargin'], rightMargin=data['rightMargin'], bottomMargin=data['bottomMargin'],
        backgroundImage=data['backgroundImage'])
    return code


def update(data: dict) -> str:
    upd(id=data['id'], name=data['name'], remark=data['remark'], paperName=data['paperName'],
        direction=data['direction'], paperWidth=data['paperWidth'], paperHeight=data['paperHeight'],
        leftMargin=data['leftMargin'], topMargin=data['topMargin'], rightMargin=data['rightMargin'],
        bottomMargin=data['bottomMargin'], backgroundImage=data['backgroundImage'])
    return data['code']


def deleteById(id: int):
    delById(id)


def findById(id: int) -> dict:
    dataList = selectById(id)
    result = {}
    if not dataList:
        return result
    keys = ['id', 'code', 'name', 'remark', 'paper_name', 'direction', 'paper_width',
            'paper_height', 'left_margin', 'right_margin', 'top_margin', 'bottom_margin', 'background_image', 'create_time']
    data = dataList[0]
    result = {k: v for k, v in zip(keys, data)}
    return result


def findByCode(code: str) -> dict:
    dataList = selectByCode(code)
    result = {}
    if not dataList:
        return result
    keys = ['id', 'code', 'name', 'remark', 'paper_name', 'direction', 'paper_width',
            'paper_height', 'left_margin', 'right_margin', 'top_margin', 'bottom_margin', 'background_image', 'create_time']
    data = dataList[0]
    result = {k: v for k, v in zip(keys, data)}
    return result


def findAll() -> list:
    return selectAll()


def findList() -> list:
    return selectList()


def findLikeByName(name: str) -> list:
    return selectLikeByName(name)


def validate(data: dict, parent: QWidget) -> bool:
    if data['name'] is None or data['name'] == '':
        MessageUtil.error(parent, '异常信息', '模板名称不能为空!')
        return False
    return True
