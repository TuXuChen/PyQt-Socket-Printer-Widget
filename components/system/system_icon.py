# coding:utf-8
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, qApp
from qfluentwidgets import FluentIcon, Theme
from common.signal_bus import signalBus


class SystemIcon(QSystemTrayIcon):

    def __init__(self, icon: QIcon, parent=None):
        super().__init__(icon, parent)

        self.roundMenu = QMenu(parent)
        showAction = QAction(QIcon(FluentIcon.ZOOM.path(Theme.LIGHT)), self.tr('显示'), parent)
        showAction.triggered.connect(self.__onShowActionTriggered)
        socketAction = QAction(QIcon(FluentIcon.GLOBE.path(Theme.LIGHT)), self.tr('Socket'), parent)
        socketAction.triggered.connect(self.__onSocketActionTriggered)
        settingAction = QAction(QIcon(FluentIcon.SETTING.path(Theme.LIGHT)), self.tr('设置'), parent)
        settingAction.triggered.connect(self.__onSettingActionTriggered)
        helpAction = QAction(QIcon(FluentIcon.HELP.path(Theme.LIGHT)), self.tr('帮助'), parent)
        helpAction.triggered.connect(self.__onHelpActionTriggered)
        quitAction = QAction(QIcon(FluentIcon.POWER_BUTTON.path(Theme.LIGHT)), self.tr('退出'), parent)
        quitAction.triggered.connect(qApp.quit)
        self.roundMenu.addActions([
            showAction,
            socketAction,
            settingAction,
            helpAction
        ])
        self.roundMenu.addSeparator()
        self.roundMenu.addAction(quitAction)

        self.setContextMenu(self.roundMenu)
        self.activated.connect(self.__onActivated)

        self.show()

    def __onActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.__onShowActionTriggered()

    def __onShowActionTriggered(self):
        signalBus.showWindowSignal.emit()

    def __onSocketActionTriggered(self):
        self.__onShowActionTriggered()
        signalBus.switchToSampleCard.emit('socketInterface', 1)

    def __onSettingActionTriggered(self):
        self.__onShowActionTriggered()
        signalBus.switchToSampleCard.emit('settingInterface', 1)

    def __onHelpActionTriggered(self):
        self.__onShowActionTriggered()
        signalBus.switchToSampleCard.emit('helpInterface', 1)
