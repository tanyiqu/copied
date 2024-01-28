
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import threading
import os
import subprocess
import pyperclip
from pynput.keyboard import Key, Controller

class ClipboardListener(QtCore.QObject):
    textChanged = QtCore.pyqtSignal(str)
    keyboard = Controller()

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.clipboard = QtWidgets.QApplication.clipboard()
        # self.clipboard.dataChanged.connect(self.onDataChanged)
        thread = threading.Thread(target=self.infinite_loop, daemon=True)

        # 启动子线程
        thread.start()
        print('thread started')

    def onDataChanged(self):
        # self.textChanged.emit(self.clipboard.text())
        self.textChanged.emit('aaa')

    def on_clipboard_change(self):
        text_content = pyperclip.paste()
        # 处理剪贴板文本内容
        # print(text_content)
        # self.notify(text_content)
        self.notify('已复制',mstr=text_content)
        # 发送键盘事件
        self.keyboard.press(Key.cmd)
        self.keyboard.press('v')
        self.keyboard.release('v')
        self.keyboard.release(Key.cmd)


    def infinite_loop(self):
        previous_content = pyperclip.paste()
        # n = 1
        while True:
            current_content = pyperclip.paste()
            if current_content != previous_content:
                self.on_clipboard_change()
                previous_content = current_content
            time.sleep(0.3)

    def notify(self,title='copied',mstr='Hello'):
        subprocess.run(['osascript', '-e', f'display notification "{mstr}" with title "{title}"'])



