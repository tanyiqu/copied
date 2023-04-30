import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import re

VERSION = 'copied 1.0'


def trim_str(s: str):
    s_new = re.sub(r"\s+", " ", s)
    return s_new
    pass


class ClipboardListener(QtCore.QObject):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.onDataChanged)

    def onDataChanged(self):
        text = "已复制：" + trim_str(self.clipboard.text())
        self.textChanged.emit(text)


class Toast(QtWidgets.QWidget):
    def __init__(self, text):
        super().__init__()

        # 设置窗口属性
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.setWindowOpacity(0.7)

        # 创建文本标签
        self.label = QtWidgets.QLabel(text)
        font = QtGui.QFont("Microsoft YaHei", 17)
        self.label.setFont(font)
        self.label.setStyleSheet(
            "color: white; background-color: #444444; padding: 10px;")
        self.label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        # 布局控件
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        # 设置窗口大小和位置
        self.resize(500, 50)
        screen_rect = QtWidgets.QApplication.desktop().availableGeometry(self)
        self.move(screen_rect.right() - self.width() - 10,
                  screen_rect.bottom() - self.height() - 20)

    def showEvent(self, event):
        # 显示窗口后 2 秒自动关闭
        QtCore.QTimer.singleShot(3000, self.close)
        super().showEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # 创建剪贴板监听器和 Toast 对象
    listener = ClipboardListener()
    toast = Toast("{} 已启动".format(VERSION))

    # 监听剪贴板变化
    listener.textChanged.connect(lambda text: toast.label.setText(text))
    listener.textChanged.connect(lambda _: toast.show())

    toast.show()

    sys.exit(app.exec_())
