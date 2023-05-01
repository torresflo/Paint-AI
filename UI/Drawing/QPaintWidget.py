from PySide6 import QtCore, QtWidgets, QtGui

from UI.Drawing.DrawUndoCommands import DrawUndoCommand

class QPaintWidget(QtWidgets.QWidget):
    onDrawImageChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_isInfillMode = False
        self.m_penWidth = 5
        self.m_penColor = QtGui.QColor(QtGui.Qt.GlobalColor.black)
        self.m_drawImage = QtGui.QImage(512, 512, QtGui.QImage.Format.Format_RGB32)

        self.m_lastImage = QtGui.QImage()
        self.m_lastPoint = QtCore.QPoint(0, 0)
        self.m_isDrawing = False
        self.m_drawingZone = QtGui.QPolygon()
        self.m_drawingZone.reserve(4096)
        self.m_undoStack = QtGui.QUndoStack()

        self.setFixedSize(512, 512)
        self.clear()

    @QtCore.Slot()
    def clear(self):
        self.m_drawImage.fill(QtGui.Qt.GlobalColor.white)
        self.m_undoStack.clear()
        self.m_drawingZone.clear()
        self.update()

    @QtCore.Slot(bool)
    def setFillMode(self, enable: bool):
        self.m_isInfillMode = enable

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MouseButton.LeftButton and not self.m_isInfillMode:
            self.m_lastImage = self.m_drawImage.copy()
            self.updateCurrentDrawingData(event.pos())
        else:
            return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() & QtCore.Qt.MouseButton.LeftButton and self.m_isDrawing:
            self.drawLineTo(self.m_lastPoint, event.pos(), self.m_penColor, self.m_penWidth)
            self.updateCurrentDrawingData(event.pos())
        else:
            return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.m_isDrawing:
                self.drawLineTo(self.m_lastPoint, event.pos(), self.m_penColor, self.m_penWidth)
                self.updateCurrentDrawingData(event.pos())
            
            else: # self.m_isInfillMode
                self.m_lastImage = self.m_drawImage.copy()
                self.fillArea(event.pos(), self.m_penColor)
            
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

    def fillArea(self, position: QtCore.QPoint, color: QtGui.QColor):
        initialColor = self.m_drawImage.pixelColor(position)
        if initialColor == color:
            return

        painter = QtGui.QPainter(self.m_drawImage)
        painter.setPen(QtGui.QPen(color, 1, QtGui.Qt.PenStyle.SolidLine, QtGui.Qt.PenCapStyle.RoundCap, QtGui.Qt.PenJoinStyle.RoundJoin))

        spanLeft = False
        spanRight = False
        pointsQueue = [position]
        while pointsQueue:
            point = pointsQueue.pop()
            x = point.x()
            y1 = point.y()

            while y1 >= 0 and self.m_drawImage.pixelColor(QtCore.QPoint(x, y1)) == initialColor :
                y1 -= 1
            y1 += 1

            minY = y1
            spanLeft = False
            spanRight = False

            while y1 < self.m_drawImage.height() and self.m_drawImage.pixelColor(QtCore.QPoint(x, y1)) == initialColor:

                if (not spanLeft) and x > 0 and self.m_drawImage.pixelColor(QtCore.QPoint(x - 1, y1)) == initialColor:
                    pointsQueue.append(QtCore.QPoint(x - 1, y1))
                    spanLeft = True
                elif spanLeft and x > 0 and self.m_drawImage.pixelColor(QtCore.QPoint(x - 1, y1)) != initialColor:
                    spanLeft = False
                
                if (not spanRight) and x < self.m_drawImage.width() - 1 and self.m_drawImage.pixelColor(QtCore.QPoint(x + 1, y1)) == initialColor:
                    pointsQueue.append(QtCore.QPoint(x + 1, y1))
                    spanRight = True
                elif spanRight and x < self.m_drawImage.width() - 1 and self.m_drawImage.pixelColor(QtCore.QPoint(x + 1, y1)) != initialColor:
                    spanRight = False

                y1 += 1
            
            painter.drawLine(QtCore.QPoint(x, minY), QtCore.QPoint(x, y1))
            self.m_drawingZone.append(QtCore.QPoint(x, minY))
            self.m_drawingZone.append(QtCore.QPoint(x, y1))

        painter.end() 
        self.pushDrawUndoCommandToStack()
    