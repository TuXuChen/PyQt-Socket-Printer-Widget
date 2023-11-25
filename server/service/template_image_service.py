# coding:utf-8
from server.mapper.template_image_mapper import (insert as add, deleteByTemplateCode as delByTemplateCode,
                                                 selectByTemplateCode)


def insert(data: dict):
    add(data['templateCode'], data['value'], data['printerType'], data['width'], data['height'], data['opacity'],
        data['xCoordinate'], data['yCoordinate'])


def deleteByTemplateCode(templateCode: str):
    delByTemplateCode(templateCode)


def findByTemplateCode(templateCode: str) -> list:
    dataList = selectByTemplateCode(templateCode)
    keys = ['id', 'template_code', 'value', 'printer_type', 'width', 'height', 'opacity', 'x_coordinate', 'y_coordinate']
    resultList = []
    if not dataList:
        return resultList
    for data in dataList:
        result = {k: v for k, v in zip(keys, data)}
        resultList.append(result)
    return resultList
