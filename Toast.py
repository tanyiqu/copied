from PyQt5 import QtCore, QtGui, QtWidgets
import re


def trim_str(s: str):
    s_new = re.sub(r"\s+", " ", s)
    return s_new
    pass


class Toast(QtWidgets.QWidget):
    def __init__(self, text):
        super().__init__()

        # 设置窗口属性
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

        self.setWindowOpacity(0.9)

        # 创建文本标签
        self.label = QtWidgets.QLabel(text)
        font = QtGui.QFont("Microsoft YaHei", 17)

        self.label.setFont(font)
        self.label.setStyleSheet(
            "color: white; background-color: #444444; padding: 10px;")
        self.label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.label.setMaximumSize(600, 50)
        # self.label.setWordWrap(True)

        # 布局控件
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        # 设置窗口大小和位置
        self.resize(600, 50)
        screen_rect = QtWidgets.QApplication.desktop().availableGeometry(self)
        # 位于屏幕右下角
        # self.move(screen_rect.right() - self.width() - 10,
        #           screen_rect.bottom() - self.height() - 20)

        # 位于屏幕左上角
        self.move(120, 40)

    def showEvent(self, event):
        # 显示窗口后自动关闭
        QtCore.QTimer.singleShot(3000, self.close)
        super().showEvent(event)
        pass

    def mousePressEvent(self, event):
        self.close()
        pass
