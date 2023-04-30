from PySide6 import QtCore, QtWidgets, QtGui

class QPaintWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_penWidth = 5
        self.m_penColor = QtGui.QColor(QtGui.Qt.GlobalColor.black)
        self.m_lastPoint = QtCore.QPoint(0, 0)
        self.m_drawing = False

        self.m_drawImage = QtGui.QImage(512, 512, QtGui.QImage.Format.Format_RGB32)

        self.setFixedSize(512, 512)

        self.clearImage()

    def clearImage(self):
        self.m_drawImage.fill(QtGui.Qt.GlobalColor.white)
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if(event.button() == QtCore.Qt.MouseButton.LeftButton):
            self.m_lastPoint = event.pos()
            self.m_drawing = True
        else:
            return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if(event.buttons() & QtCore.Qt.MouseButton.LeftButton and self.m_drawing):
            self.drawLineTo(event.pos())
        else:
            return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if(event.button() == QtCore.Qt.MouseButton.LeftButton and self.m_drawing):
            self.drawLineTo(event.pos())
            self.m_drawing = False
        else:
            return super().mouseReleaseEvent(event)
        
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.drawImage(event.rect(), self.m_drawImage, event.rect())
        painter.end()

    def drawLineTo(self, point: QtCore.QPoint):
        painter = QtGui.QPainter(self.m_drawImage)
        painter.setPen(QtGui.QPen(self.m_penColor, self.m_penWidth, QtGui.Qt.PenStyle.SolidLine, QtGui.Qt.PenCapStyle.RoundCap, QtGui.Qt.PenJoinStyle.RoundJoin))
        painter.drawLine(self.m_lastPoint, point)
        painter.end()

        radius = (self.m_penWidth / 2) + 2
        self.update(QtCore.QRect(self.m_lastPoint, point).normalized().adjusted(-radius, -radius, radius, radius))

        self.m_lastPoint = point
    