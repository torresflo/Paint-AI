from PySide6 import QtCore, QtGui

class QPaintWidget:
    pass

class DrawUndoCommand(QtGui.QUndoCommand):
    def __init__(self, paintWidget: QPaintWidget, drawPosition: QtCore.QPoint, previousImage: QtGui.QImage, drawingImage: QtGui.QImage, parent=None):
        super().__init__(parent)
        self.m_paintWidget = paintWidget
        self.m_previousImage = previousImage
        self.m_drawPosition = drawPosition
        self.m_drawingImage = drawingImage

    def undo(self):
        self.m_paintWidget.drawImage(self.m_drawPosition, self.m_previousImage)

    def redo(self):
        self.m_paintWidget.drawImage(self.m_drawPosition, self.m_drawingImage)
