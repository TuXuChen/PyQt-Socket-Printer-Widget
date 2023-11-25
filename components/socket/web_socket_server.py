# coding:utf-8
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QHostAddress
from PyQt5.QtWebSockets import QWebSocketServer


class WebSocketServer(QWebSocketServer):
    textMessage = pyqtSignal(str)
    binaryMessage = pyqtSignal(str)
    connectionMessage = pyqtSignal()

    def __init__(self, parent=None):
        super(WebSocketServer, self).__init__("WebSocketServer", QWebSocketServer.NonSecureMode, parent)
        self.clients = []
        # 新增的标识符，默认为关闭状态
        self.is_running = False
        self.newConnection.connect(self.__onNewConnection)

    def startServer(self, address: str, port: int):
        # 启动服务器
        if not self.is_running:
            if self.listen(QHostAddress(address), port):
                self.is_running = True
                print(f"WebSocket server is listening on {address}:{port}.")
            else:
                print(f"Error: {self.errorString()}")

    def stopServer(self):
        # 关闭服务器
        if self.is_running:
            self.close()
            self.is_running = False
            print("WebSocket server stopped.")

    def __onNewConnection(self):
        client_socket = self.nextPendingConnection()
        client_socket.textMessageReceived.connect(self.__onProcessTextMessageReceived)
        client_socket.binaryMessageReceived.connect(self.__onProcessBinaryMessageReceived)
        client_socket.disconnected.connect(self.__onDisconnected)

        self.clients.append(client_socket)
        print(f"Client connected. Total clients: {len(self.clients)}")
        self.connectionMessage.emit()

    def __onProcessTextMessageReceived(self, message):
        # 处理文本消息
        print(f"Text message received: {message}")
        self.textMessage.emit(message)

    def __onProcessBinaryMessageReceived(self, message):
        # 处理二进制消息
        print(f"Binary message received: {message}")
        self.binaryMessage.emit(message)

    def __onDisconnected(self):
        client_socket = self.sender()
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            print(f"Client disconnected. Total clients: {len(self.clients)}")
