from ui.Forms.pyuic.Ui_MainForm import Ui_MainForm
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget, QAbstractItemView, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon, QPixmap
import copied
import base64
import re

from ClipboardListener import ClipboardListener


class MainForm(QWidget):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.mainForm = Ui_MainForm()
        self.mainForm.setupUi(self)

        # 创建系统托盘对象
        self.tray_icon = QSystemTrayIcon(self)
        base64_data = 'data:image/png;base64,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'
        # 创建 QPixmap 对象
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(base64_data.split(",")[1]))

        # 创建 QIcon 对象
        self.tray_icon.setIcon(QIcon(pixmap))
        self.tray_icon.setToolTip('copied 正在运行')

        # 创建右键菜单
        self.menu = QMenu(self)
        show_action = QAction('显示窗口', self)
        show_action.triggered.connect(self.show_window)
        quit_action = QAction('退出', self)
        quit_action.triggered.connect(lambda: exit(0))
        self.menu.addAction(show_action)
        self.menu.addAction(quit_action)

        # 点击图标显示主窗口
        self.tray_icon.activated.connect(self.onTrayActivated)

        # 将右键菜单设置为托盘对象的菜单
        self.tray_icon.setContextMenu(self.menu)

        # 将窗口隐藏到系统托盘中
        self.hide()
        self.tray_icon.show()

        self.run_listen()

        pass

    def show_window(self):
        """将窗口从系统托盘中恢复并显示在屏幕上"""
        self.showNormal()
        self.activateWindow()

        # 点击图标显示主窗口

    def onTrayActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if not self.isVisible():
                self.show()
        pass

    def trim_str(self, s: str):
        s_new = re.sub(r"\s+", " ", s)
        s_new = "已复制：" + s_new
        return s_new
        pass

    def run_listen(self):
        # 创建剪贴板监听器和 Toast 对象
        self.listener = ClipboardListener()
        toast = copied.Toast("{} 已启动".format(copied.VERSION))

        # 监听剪贴板变化
        self.listener.textChanged.connect(
            lambda text: toast.label.setText(self.trim_str(text)))
        self.listener.textChanged.connect(lambda _: toast.show())

        toast.show()
        pass

    pass
