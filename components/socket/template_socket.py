# coding:utf-8
import json
from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWebSockets import QWebSocket

from common.signal_bus import signalBus
from components.custom.preview_view import PreviewCardView
from components.socket.web_socket_server import WebSocketServer
from config.config import cfg
from common.message_util import MessageUtil


def handleMessage(messageJson: str):
    try:
        dataDict = json.loads(messageJson)
        if not dataDict:
            return
        preview = PreviewCardView()
        preview.initContentWidget(dataDict)
        signalBus.showWindowSignal.emit()
        preview.exec_()
    except Exception as e:
        pass


class TemplateWebSocket(QObject):

    def __init__(self, parent: QWidget = None):
        super().__init__()
        self.webSocket = QWebSocket()
        self.parentWidget = parent

        self.webSocket.connected.connect(self.__onWebSocketConnected)
        self.webSocket.textMessageReceived.connect(self.__onWebSocketTextMessageReceived)

    def initConnection(self):
        address = cfg.SocketAddress.value
        self.closeConnection()
        self.webSocket.open(QUrl(address))

    def closeConnection(self):
        self.webSocket.close()

    def __onWebSocketConnected(self):
        MessageUtil.success(self.parentWidget, self.tr('WebSocket连接服务器成功'), self.tr(''), duration=-1)

    def __onWebSocketTextMessageReceived(self, message: str):
        MessageUtil.success(self.parentWidget, self.tr('客户端接收到服务器的消息'), self.tr(''))
        print(message)
        handleMessage(message)


class TemplateTcpSocket(QObject):

    def __init__(self, parent: QWidget = None):
        super().__init__()
        self.tcpSocket = QTcpSocket(self)
        self.parentWidget = parent

        self.tcpSocket.connected.connect(self.__onTcpSocketConnected)
        self.tcpSocket.readyRead.connect(self.__onTcpSocketReadyRead)

    def initConnection(self):
        self.closeConnection()
        self.tcpSocket.connectToHost(cfg.TcpHost.value, cfg.TcpPort.value)

    def closeConnection(self):
        self.tcpSocket.close()

    def writeConnection(self, content: str):
        message = content.encode()
        self.tcpSocket.write(message)

    def __onTcpSocketConnected(self):
        MessageUtil.success(self.parentWidget, self.tr('Tcp连接服务器成功'), self.tr(''), duration=-1)

    def __onTcpSocketReadyRead(self):
        while self.tcpSocket.bytesAvailable():
            datagram = self.tcpSocket.read(self.tcpSocket.bytesAvailable())
            message = datagram.decode()
            MessageUtil.success(self.parentWidget, self.tr('客户端接收到服务器的消息'), self.tr(''))
            print(message)
            handleMessage(message)


class TemplateWebSocketServer(QObject):

    def __init__(self, parent: QWidget = None):
        super().__init__()
        self.webSocketServer = WebSocketServer()
        self.parentWidget = parent

        self.webSocketServer.textMessage.connect(self.__onTextMessage)
        self.webSocketServer.connectionMessage.connect(self.__onConnectionMessage)

    def startServer(self):
        self.webSocketServer.startServer(cfg.get(cfg.SocketServerHost), cfg.get(cfg.SocketServerPort))
        MessageUtil.success(self.parentWidget, self.tr('启动SocketServer服务成功'), self.tr(''), duration=-1)

    def stopServer(self):
        self.webSocketServer.stopServer()
        MessageUtil.success(self.parentWidget, self.tr('关闭SocketServer服务成功'), self.tr(''), duration=-1)

    def __onConnectionMessage(self):
        MessageUtil.success(self.parentWidget, self.tr('连接SocketServer成功'), self.tr(''), duration=-1)

    def __onTextMessage(self, message):
        MessageUtil.success(self.parentWidget, self.tr('SocketServer接收到消息'), self.tr(''))
        handleMessage(message)
