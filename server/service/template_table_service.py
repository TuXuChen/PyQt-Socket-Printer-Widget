# coding:utf-8
from server.mapper.template_table_mapper import (insert as add, deleteByTemplateCode as delByTemplateCode,
                                                 selectByTemplateCode)


def insert(data: dict):
    add(data['templateCode'], data['columnCount'], data['rowCount'], data['showGrid'], data['frameShape'],
        data['mergedCells'], data['row'], data['column'], data['value'], data['cellAlignment'], data['cellWidth'],
        data['cellHeight'], data['cellFontFamily'], data['cellFontColor'], data['cellFontSize'], data['cellFontItalic'],
        data['cellFontBold'], data['cellFontUnderline'], data['width'], data['height'], data['xCoordinate'],
        data['yCoordinate'])


def deleteByTemplateCode(templateCode: str):
    delByTemplateCode(templateCode)


def findByTemplateCode(templateCode: str) -> list:
    dataList = selectByTemplateCode(templateCode)
    keys = ['id', 'template_code', 'value', 'column_count', 'row_count', 'show_grid', 'frame_shape', 'merged_cells',
            'row', 'column', 'cell_alignment', 'cell_width', 'cell_height', 'cell_font_family',
            'cell_font_color', 'cell_font_size', 'cell_font_italic', 'cell_font_bold', 'cell_font_underline', 'width',
            'height', 'x_coordinate', 'y_coordinate']
    resultList = []
    if not dataList:
        return resultList
    for data in dataList:
        result = {k: v for k, v in zip(keys, data)}
        resultList.append(result)
    return resultList


def getStructure(templateCode: str) -> list:
    dataList = selectByTemplateCode(templateCode)
    result = []
    if not dataList:
        return result
    columnCount = dataList[0][3]
    currentColumn = 1
    currentColumnData = {}
    for data in dataList:
        value = data[2]
        if value.startswith("#") and value.endswith("#"):
            field = value[1:-1]
            currentColumnData[field] = ''

        if currentColumn == columnCount:
            currentColumn = 1
            if currentColumnData:
                result.append(currentColumnData)
                currentColumnData = {}
        else:
            currentColumn += 1

    return result
