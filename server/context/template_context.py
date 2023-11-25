# coding:utf-8
import json
from enum import Enum
from server.service.template_label_service import (getStructure as labelGetStructure,
                                                   findByTemplateCode as labelByTemplateCode)
from server.service.template_image_service import findByTemplateCode as imageByTemplateCode
from server.service.template_table_service import (getStructure as tableGetStructure,
                                                   findByTemplateCode as tableByTemplateCode)


class TemplateType(Enum):
    LABEL = 'label',
    IMAGE = 'image',
    TABLE = 'table'


class TemplateContext:

    @staticmethod
    def getStructure(templateCode: str) -> str:
        """
        获取模板数据结构
        :param templateCode:
        :return:
        """
        result = labelGetStructure(templateCode)
        result['templateCode'] = templateCode
        result['list'] = tableGetStructure(templateCode)
        return json.dumps(result, indent=4)

    @staticmethod
    def loadStructure(templateCode: str, templateType: TemplateType, renderData: dict = None, page: int = 1) -> list:
        """
        获取模板数据
        :param renderData:
        :param templateCode:
        :param templateType:
        :param page:
        :return:
        """
        match templateType:
            case TemplateType.LABEL:
                dataList = labelByTemplateCode(templateCode)
                if not renderData:
                    return dataList
                for data in dataList:
                    if data['value'].startswith("@") and data['value'].endswith("@"):
                        field = data['value'][1:-1]
                        if field in renderData.keys():
                            newValue = renderData[field]
                            data['value'] = newValue
                return dataList
            case TemplateType.IMAGE:
                dataList = imageByTemplateCode(templateCode)
                return dataList
            case TemplateType.TABLE:
                dataList = tableByTemplateCode(templateCode)
                if not renderData:
                    return dataList
                renderList = renderData['list']
                columnCount = dataList[0]['column_count']
                rowCount = dataList[0]['row_count']
                start_index = (page - 1) * rowCount
                end_index = start_index + rowCount
                pageData = renderList[start_index:end_index]
                currentColumn = 0
                for row in range(len(dataList)):
                    data = dataList[row]
                    if row != 0 and row % columnCount == 0:
                        currentColumn += 1
                    if data['value'].startswith("#") and data['value'].endswith("#"):
                        field = data['value'][1:-1]
                        dataColumn = currentColumn - 1
                        if pageData and len(pageData) > dataColumn and field in pageData[dataColumn].keys():
                            newValue = pageData[dataColumn][field]
                            data['value'] = newValue
                        else:
                            data['value'] = ''
                return dataList

