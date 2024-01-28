
from PyQt5 import QtCore, QtGui, QtWidgets


class ClipboardListener(QtCore.QObject):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.onDataChanged)

    def onDataChanged(self):
        self.textChanged.emit(self.clipboard.text())
