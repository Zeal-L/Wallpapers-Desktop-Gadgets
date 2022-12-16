import random
import sys

from PySide6 import QtCore, QtGui, QtWidgets

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)



class MainWindow(QtWidgets.QWidget, QtGui.QCloseEvent):
    
    isOnRankingWindow = None
    
    def __init__(self, manager):
        super().__init__()
        self.setWindowTitle("WDG桌面壁纸组件 0.0.1")
        self.resize(400, 400)
        self.setup_ui()
        self.manager = manager
        

    def setup_ui(self) -> None:
        self.button = QtWidgets.QPushButton("P站热门排名")
        self.button.clicked.connect(self.openRankingWindow)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)
        

    @QtCore.Slot()
    def openRankingWindow(self) -> None:
        if self.isOnRankingWindow is None:
            self.isOnRankingWindow = RankingWindow(self, self.manager)
            self.isOnRankingWindow.show()
            
        self.isOnRankingWindow.activateWindow()

    
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.isOnRankingWindow is not None:
            self.isOnRankingWindow = None


class RankingWindow(QtWidgets.QWidget):
    def __init__(self, mainWindow: MainWindow, manager):
        super().__init__()
        self.setWindowTitle("P站热门排名")
        self.resize(500, 600)
        self.mainWindow = mainWindow
        self.manager = manager

        # 获取主窗口的坐标
        main_window_x, main_window_y = mainWindow.pos().x(), mainWindow.pos().y()
        # 获取当前屏幕的宽度和高度
        screen_rect = QtWidgets.QApplication.instance().screens()[0].geometry()
        screen_width, screen_height = screen_rect.width(), screen_rect.height()
        # 计算次窗口的坐标
        if main_window_x + mainWindow.width() + self.width() <= screen_width:
            # 如果当前屏幕右边有空间，则在mainWindow窗口的右边创建rankingWindow
            self.move(main_window_x + mainWindow.width()+20, main_window_y-20)
        else:
            # 如果当前屏幕右边没有空间，则在mainWindow窗口的左边创建rankingWindow
            self.move(main_window_x - self.width()-20, main_window_y-20)
        
        self.setup_ui()
        
    def setup_ui(self) -> None:
        
        rankInfo = self.manager.showRankings()
        
        self.layout = QtWidgets.QGridLayout(self)
        
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 800, 1100))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        for num, item in enumerate(rankInfo, start=1):
            self.add_line(num, item)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.layout.addWidget(self.scrollArea, 0, 0, 0, 0)
        
    def add_line(self, num, item) -> None:
        pid, title, artist = item
        label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        label.setMinimumSize(300, 25)
        label.setText(f'''<a style="font-family: 微软雅黑; color: #000000; font-size: 12pt;  text-decoration: none" href="https://www.pixiv.net/artworks/{pid}">No.{num} -- {title} -- by {artist}</a>''')
        label.setOpenExternalLinks(True)
        label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        
        self.verticalLayout.addWidget(label)
        
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.mainWindow.isOnRankingWindow is not None:
            self.mainWindow.isOnRankingWindow = None

