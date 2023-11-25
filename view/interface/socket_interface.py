# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame
from qfluentwidgets import (ExpandLayout, SettingCardGroup,
                            SwitchSettingCard, FluentIcon, ScrollArea)

from common.message_util import MessageUtil
from config.config import cfg
from view.interface.gallery_interface import GalleryInterface
from components.card.host_edit_setting_card import HostEditSettingCard
from components.card.socket_setting_card import SocketSettingCard
from components.socket.template_socket import TemplateTcpSocket, TemplateWebSocket, TemplateWebSocketServer


class SocketCardView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('socketCardView')
        self.tcpSocket = TemplateTcpSocket(parent)
        self.webSocket = TemplateWebSocket(parent)
        self.webServerSocket = TemplateWebSocketServer(parent)
        self.view = QFrame(self)
        self.openWebServerGroup = SettingCardGroup(self.tr("SocketServer"), self.view)
        self.openWebServerCard = SwitchSettingCard(
            FluentIcon.UPDATE,
            self.tr('启动SocketServer服务'),
            self.tr('打开将启动Socket服务器,并等待客户端请求'),
            parent=self.openWebServerGroup
        )
        self.settingWebServerCard = HostEditSettingCard(
            cfg.SocketServerHost.value,
            cfg.SocketServerPort.value,
            FluentIcon.SETTING,
            self.tr('设置SocketServer服务'),
            self.tr('通过此处设置服务器地址及端口号'),
            self.openWebServerGroup
        )
        self.openWebGroup = SettingCardGroup(self.tr("Socket连接"), self.view)
        self.openWebCard = SwitchSettingCard(
            FluentIcon.UPDATE,
            self.tr('打开Socket连接'),
            self.tr('打开将尝试连接服务器,并等待服务器请求'),
            parent=self.openWebGroup
        )
        self.settingWebCard = SocketSettingCard(
            cfg.SocketAddress.value,
            FluentIcon.SETTING,
            self.tr('设置Socket连接'),
            self.tr('通过此处设置需要连接的服务器地址及端口号'),
            self.openWebGroup
        )

        self.openTcpGroup = SettingCardGroup(self.tr("Tcp连接"), self.view)
        self.openTcpCard = SwitchSettingCard(
            FluentIcon.UPDATE,
            self.tr('打开Tcp连接'),
            self.tr('打开将尝试连接服务器,并等待服务器请求'),
            parent=self.openTcpGroup
        )
        self.settingTcpCard = HostEditSettingCard(
            cfg.TcpHost.value,
            cfg.TcpPort.value,
            FluentIcon.SETTING,
            self.tr('设置Tcp连接'),
            self.tr('通过此处设置需要连接的服务器地址及端口号'),
            self.openTcpGroup
        )

        self.openWebServerGroup.addSettingCard(self.openWebServerCard)
        self.openWebServerGroup.addSettingCard(self.settingWebServerCard)

        self.openWebGroup.addSettingCard(self.openWebCard)
        self.openWebGroup.addSettingCard(self.settingWebCard)

        self.openTcpGroup.addSettingCard(self.openTcpCard)
        self.openTcpGroup.addSettingCard(self.settingTcpCard)

        self.expandLayout = ExpandLayout(self.view)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(5, 10, 5, 10)
        self.expandLayout.addWidget(self.openWebServerGroup)
        self.expandLayout.addWidget(self.openWebGroup)
        self.expandLayout.addWidget(self.openTcpGroup)

        self.setFixedSize(850, 1200)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setStyleSheet('background-color: transparent;')

        self.openWebServerCard.checkedChanged.connect(self.__onOpenWebServerCardChecked)
        self.openWebCard.checkedChanged.connect(self.__onOpenWebCardChecked)
        self.openTcpCard.checkedChanged.connect(self.__onOpenTcpCardChecked)

        self.settingWebServerCard.confirmClicked.connect(self.__onSettingWebServerCardConfirmClicked)
        self.settingWebCard.confirmClicked.connect(self.__onSettingWebCardConfirmClicked)
        self.settingTcpCard.confirmClicked.connect(self.__onSettingTcpCardConfirmClicked)

    def __onOpenWebServerCardChecked(self, on: bool):
        if on:
            self.webServerSocket.startServer()
        else:
            self.webServerSocket.stopServer()

    def __onOpenTcpCardChecked(self, on: bool):
        if on:
            self.tcpSocket.initConnection()
        else:
            self.tcpSocket.closeConnection()

    def __onOpenWebCardChecked(self, on: bool):
        if on:
            self.webSocket.initConnection()
        else:
            self.webSocket.closeConnection()

    def __onSettingWebCardConfirmClicked(self, address: str):
        cfg.set(cfg.SocketAddress, address)
        MessageUtil.success(self.parent(), self.tr('连接设置成功!'), self.tr(''))

    def __onSettingTcpCardConfirmClicked(self, ip: str, port: int):
        cfg.set(cfg.TcpHost, ip)
        cfg.set(cfg.TcpPort, port)
        MessageUtil.success(self.parent(), self.tr('连接设置成功!'), self.tr(''))

    def __onSettingWebServerCardConfirmClicked(self, ip: str, port: int):
        cfg.set(cfg.SocketServerPort, ip)
        cfg.set(cfg.SocketServerPort, port)
        MessageUtil.success(self.parent(), self.tr('服务配置成功!'), self.tr(''))


class SocketInterface(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title="WebSocket",
            subtitle="使用webSocket连接服务器",
            parent=parent
        )
        self.setObjectName('socketInterface')

        # 隐藏父类的文档说明按钮
        self.toolBar.separator.hide()
        self.toolBar.helpButton.hide()

        self.socketView = SocketCardView(self)
        self.vBoxLayout.addWidget(self.socketView, 0, Qt.AlignTop)
