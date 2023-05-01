from PySide6 import QtCore, QtWidgets, QtGui

from UI.Drawing.DrawingUndoCommands import DrawUndoCommand

class QPaintWidget(QtWidgets.QWidget):
    onDrawImageChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_penWidth = 5
        self.m_penColor = QtGui.QColor(QtGui.Qt.GlobalColor.black)
        self.m_lastPoint = QtCore.QPoint(0, 0)
        self.m_isDrawing = False

        self.m_undoStack = QtGui.QUndoStack()
        self.m_drawingZone = QtGui.QPolygon()
        self.m_drawingZone.reserve(4096)

        self.m_drawImage = QtGui.QImage(512, 512, QtGui.QImage.Format.Format_RGB32)
        self.m_lastImage = self.m_drawImage.copy()

        self.setFixedSize(512, 512)
        self.clearImage()

    def clearImage(self):
        self.m_drawImage.fill(QtGui.Qt.GlobalColor.white)
        self.update()

    def loadImage(self, image: QtGui.QImage):
        painter = QtGui.QPainter(self.m_drawImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        painter.end()
        self.onDrawImageChanged.emit()
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if(event.button() == QtCore.Qt.MouseButton.LeftButton):
            self.m_lastImage = self.m_drawImage.copy()
            self.updateCurrentDrawingData(event.pos())
        else:
            return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if(event.buttons() & QtCore.Qt.MouseButton.LeftButton and self.m_isDrawing):
            self.drawLineTo(self.m_lastPoint, event.pos(), self.m_penColor, self.m_penWidth)
            self.updateCurrentDrawingData(event.pos())
        else:
            return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if(event.button() == QtCore.Qt.MouseButton.LeftButton and self.m_isDrawing):
            self.drawLineTo(self.m_lastPoint, event.pos(), self.m_penColor, self.m_penWidth)
            self.updateCurrentDrawingData(event.pos())
            self.pushDrawUndoCommandToStack()
        else:
            return super().mouseReleaseEvent(event)
        
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.drawImage(event.rect(), self.m_drawImage, event.rect())
        painter.end()

    def updateCurrentDrawingData(self, drawPoint: QtCore.QPoint):
        self.m_isDrawing = True
        self.m_lastPoint = drawPoint
        self.m_drawingZone.append(self.m_lastPoint)

    def pushDrawUndoCommandToStack(self):
        drawingRect = self.m_drawingZone.boundingRect()
        radius = (self.m_penWidth / 2) + 2
        drawingRect = drawingRect.normalized().adjusted(-radius, -radius, radius, radius)
        command = DrawUndoCommand(self, drawingRect.topLeft(), self.m_lastImage.copy(drawingRect), self.m_drawImage.copy(drawingRect))
        self.m_undoStack.push(command)

        self.m_isDrawing = False
        self.m_drawingZone.clear()
        self.onDrawImageChanged.emit()

    def drawLineTo(self, fromPoint: QtCore.QPoint, toPoint: QtCore.QPoint, penColor: QtGui.QColor, penWidth: int):
        painter = QtGui.QPainter(self.m_drawImage)
        painter.setPen(QtGui.QPen(penColor, penWidth, QtGui.Qt.PenStyle.SolidLine, QtGui.Qt.PenCapStyle.RoundCap, QtGui.Qt.PenJoinStyle.RoundJoin))
        painter.drawLine(fromPoint, toPoint)
        painter.end()

        radius = (self.m_penWidth / 2) + 2
        self.update(QtCore.QRect(self.m_lastPoint, fromPoint).normalized().adjusted(-radius, -radius, radius, radius))

    def drawImage(self, position: QtCore.QPoint, image: QtGui.QImage):
        painter = QtGui.QPainter(self.m_drawImage)
        painter.drawImage(position, image)
        painter.end()

        rightBottomPosition = QtCore.QPoint(position.x() + image.width(), position.y() + image.height())
        self.update(QtCore.QRect(position, rightBottomPosition))
    