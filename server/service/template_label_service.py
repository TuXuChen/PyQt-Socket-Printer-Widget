# coding:utf-8
from server.mapper.template_label_mapper import (insert as add, deleteByTemplateCode as delByTemplateCode,
                                                 selectByTemplateCode)


def insert(data: dict):
    add(data['templateCode'], data['value'], data['printerType'], data['border'], data['borderSize'], data['borderType'], data['width'], data['height'],
        data['xCoordinate'], data['yCoordinate'], data['fontSize'], data['fontFamily'], data['fontColor'], data['fontItalic'], data['fontBold'],
        data['fontUnderline'], data['fontAlignment'])


def deleteByTemplateCode(templateCode: str):
    delByTemplateCode(templateCode)


def findByTemplateCode(templateCode: str) -> list:
    dataList = selectByTemplateCode(templateCode)
    keys = ['id', 'template_code', 'value', 'printer_type', 'border', 'border_size', 'border_type', 'width', 'height',
            'x_coordinate', 'y_coordinate', 'font_size', 'font_family', 'font_color', 'font_italic', 'font_bold',
            'font_underline', 'font_alignment']
    resultList = []
    if not dataList:
        return resultList
    for data in dataList:
        result = {k: v for k, v in zip(keys, data)}
        resultList.append(result)
    return resultList


def getStructure(templateCode: str) -> dict:
    dataList = selectByTemplateCode(templateCode)
    result = {}
    if dataList:
        for data in dataList:
            value = data[2]
            if value.startswith("@") and value.endswith("@"):
                field = value[1:-1]
                result[field] = ''
        return result
    return {}


def loadStructure(templateCode: str, data: dict):
    pass
