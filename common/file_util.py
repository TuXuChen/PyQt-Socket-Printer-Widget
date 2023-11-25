import os
import shutil
import requests
from config.config import cfg
from PyQt5.QtCore import QIODevice, QFile
from common.random_util import getRandom, getCode


def readResourceFile(file_path):
    resource_file = QFile(file_path)

    if not resource_file.open(QIODevice.ReadOnly | QIODevice.Text):
        print("Failed to open resource file.")
        return None

    content = resource_file.readAll()
    return bytes(content).decode("utf-8")


def getFolderSize(folder_path) -> str:
    """ 计算文件夹大小 """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if total_size < 1024.0:
            return "%3.1f %s" % (total_size, x)
        total_size /= 1024.0


def deleteFilesInFolder(folder_path):
    """ 清除文件夹内的所有文件 """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def downloadImage(url: str) -> str:
    """ 下载网络图片并保存 如果不是网路图片则直接返回 """
    if url.startswith('http'):
        filename = getRandom() + '.jpg'
        save_path = cfg.get(cfg.cacheFolder) + '/' + filename
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
        return save_path
    else:
        return url


def copyImage(filePath: str) -> str:
    saveFilePath = cfg.get(cfg.fileFolder)
    saveFilePath += "/" + getCode() + ".jpg"
    shutil.copy(filePath, saveFilePath)
    # 找到文件名的起始位置
    index = saveFilePath.find('system')
    # 获取 system 后的部分
    relative_path = saveFilePath[index:]
    relative_path = "./" + relative_path
    return relative_path
