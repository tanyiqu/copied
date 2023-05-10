import sys
import copied
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.Forms.MainForm import MainForm


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainForm()
    sys.exit(app.exec_())
    pass