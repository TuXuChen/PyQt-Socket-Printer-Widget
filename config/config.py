# coding:utf-8
from enum import Enum

from PyQt5.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator, ConfigSerializer, __version__)

from components.validator.int_validator import IntConfigValidator


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    """ Config of application """

    # folders
    musicFolders = ConfigItem(
        "Folders", "LocalMusic", [], FolderListValidator())
    downloadFolder = ConfigItem(
        "Folders", "Download", "system/download", FolderValidator())
    cacheFolder = ConfigItem(
        "Folders", "Cache", "system/cache", FolderValidator())
    fileFolder = ConfigItem("Folders", "File", "system/file", FolderValidator())

    # main window
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)
    isRemind = ConfigItem("MainWindow", "IsRemind", True, BoolValidator())

    # Material
    blurRadius = RangeConfigItem("Material", "AcrylicBlurRadius", 15, RangeValidator(0, 40))

    # software update
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())

    SocketAddress = ConfigItem("Socket", "Address", "127.0.0.1:8080")

    TcpHost = ConfigItem("Tcp", "Host", "127.0.0.1")
    TcpPort = ConfigItem("Tcp", "Port", 6666, IntConfigValidator(6666))

    SocketServerHost = ConfigItem("SocketServer", "Host", "127.0.0.1")
    SocketServerPort = ConfigItem("Socket", "Port", 8888, IntConfigValidator(8888))


YEAR = 2023
AUTHOR = "tuYooo"
VERSION = __version__

cfg = Config()
qconfig.load('config/config.json', cfg)