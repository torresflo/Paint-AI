from PySide6 import QtCore
from PySide6 import QtWidgets, QtGui

from UI.QClickableLabel import QClickableLabel

class QColorLabel(QClickableLabel): 
    onColorChanged = QtCore.Signal(QtGui.QColor)

    def __init__(self, color: QtGui.QColor, parent=None):
        super().__init__(parent)
        self.updateColor(color)

    def updateColor(self, color: QtGui.QColor):
        self.m_color = color
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.m_color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.onColorChanged.emit(self.m_color)