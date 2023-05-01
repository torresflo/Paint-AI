import sys
from PySide6 import QtWidgets, QtGui

from UI.MainWindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    mainWindow = MainWindow()
    mainWindow.setWindowTitle("Paint AI")
    mainWindow.setWindowIcon(QtGui.QIcon("Resources/icon.png"))
    mainWindow.show()
    sys.exit(app.exec())
