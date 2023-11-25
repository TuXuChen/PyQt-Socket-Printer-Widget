# coding: utf-8
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (FluentIcon as FIF, NavigationItemPosition, FluentWindow, SplashScreen)

from view.interface.gallery_interface import GalleryInterface
from view.interface.home_interface import HomeInterface
from view.interface.socket_interface import SocketInterface
from view.interface.setting_interface import SettingInterface
from view.interface.paper_interface import PaperInterface
from view.interface.template_interface import TemplateInterFace
from view.interface.code_interface import CodeInterface
from view.interface.help_interface import HelpInterface
from common.signal_bus import signalBus
from components.system.system_icon import SystemIcon
from components.dialog.message_dialog import MessageDialog
from config.config import cfg
from common import resource


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.systemIcon = QIcon(':/gallery/images/logo.png')
        self.trayIcon = SystemIcon(self.systemIcon, self)
        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.socketInterface = SocketInterface(self)
        self.settingInterface = SettingInterface(self)
        self.paperInterface = PaperInterface(self)
        self.templateInterFace = TemplateInterFace(self)
        self.codeInterFace = CodeInterface(self)
        self.helpInterFace = HelpInterface(self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(self.systemIcon)
        self.setWindowTitle('PyQt-Socket-Printer-Widget')
        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def initLayout(self):
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.showWindowSignal.connect(self.showWindow)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('首页'))
        self.addSubInterface(self.socketInterface, FIF.GLOBE, self.tr('socket'))
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.paperInterface, FIF.DOCUMENT, self.tr('纸张'))
        self.addSubInterface(self.templateInterFace, FIF.PALETTE, self.tr('模板设计'))
        self.addSubInterface(self.codeInterFace, FIF.CODE, self.tr('数据结构'))
        self.addSubInterface(self.helpInterFace, FIF.HELP, self.tr('文档说明'))

        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('设置'), NavigationItemPosition.BOTTOM)

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren((GalleryInterface, SettingInterface,))
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                # w.scrollToCard(index)

    def showWindow(self):
        self.show()

    def closeEvent(self, event):
        """ 重写关闭事件，将窗口最小化到系统托盘 """
        event.ignore()
        isRemind = cfg.get(cfg.isRemind)
        if isRemind:
            w = MessageDialog(self)
            if w.exec():
                self.hide()
        else:
            self.hide()
