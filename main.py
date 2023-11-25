# coding:utf-8
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from config.config import cfg
from view.window.main_window import MainWindow

# enable dpi scale
if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# internationalization
# locale = cfg.get(cfg.language).value
# translator = FluentTranslator(locale)
# galleryTranslator = QTranslator()
# galleryTranslator.load(locale, "gallery", ".", ":/gallery/i18n")
# 创建翻译器实例，生命周期必须和 app 相同
translator = FluentTranslator(QLocale(QLocale.Chinese, QLocale.China))
app.installTranslator(translator)

# create main window
w = MainWindow()
w.show()

app.exec_()

# 打包命令 pyinstaller --onefile main.py
