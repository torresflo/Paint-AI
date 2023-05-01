from PySide6 import QtCore, QtGui, QtWidgets

from UI.QClickableLabel import QClickableLabel
from UI.Drawing.QColorLabel import QColorLabel

DefaultColorsFirstRow = [
    QtGui.QColor(0, 0, 0), 
    QtGui.QColor(64, 64, 64),
    QtGui.QColor(255, 0, 0),
    QtGui.QColor(255, 106, 0),
    QtGui.QColor(255, 216, 0),
    QtGui.QColor(182, 255, 0),
    QtGui.QColor(76, 255, 0),
    QtGui.QColor(0, 255, 33),
    QtGui.QColor(0, 255, 144),
    QtGui.QColor(0, 255, 255),
    QtGui.QColor(0, 148, 255),
    QtGui.QColor(0, 38, 255),
    QtGui.QColor(75, 0, 255),
    QtGui.QColor(178, 0, 255),
    QtGui.QColor(255, 0, 220),
    QtGui.QColor(255, 0, 110)
    ]

DefaultColorsSecondRow = [
    QtGui.QColor(255, 255, 255), 
    QtGui.QColor(128, 128, 128),
    QtGui.QColor(127, 0, 0),
    QtGui.QColor(127, 51, 0),
    QtGui.QColor(127, 106, 0),
    QtGui.QColor(91, 127, 0),
    QtGui.QColor(38, 127, 0),
    QtGui.QColor(0, 127, 14),
    QtGui.QColor(0, 127, 70),
    QtGui.QColor(0, 127, 127),
    QtGui.QColor(0, 74, 127),
    QtGui.QColor(0, 19, 127),
    QtGui.QColor(33, 0, 127),
    QtGui.QColor(87, 0, 127),
    QtGui.QColor(127, 0, 110),
    QtGui.QColor(127, 0, 55)
    ]             

class QPaintOptionsWidget(QtWidgets.QWidget):
    onSelectedColorChangedSignal = QtCore.Signal(QtGui.QColor)
    onSelectedWidthChangedSignal = QtCore.Signal(int)
    onSelectedFillModeChangedSignal = QtCore.Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # Fill mode
        self.m_fillPushButton = QtWidgets.QPushButton(QtGui.QIcon("Resources/fill.png"), "")
        self.m_fillPushButton.setCheckable(True)
        self.m_fillPushButton.setFixedSize(32, 32)
        self.m_fillPushButton.clicked.connect(self.onSelectedFillModeChangedSignal)

        # Selected width
        self.m_selectedWidthSpinBox = QtWidgets.QSpinBox()
        self.m_selectedWidthSpinBox.setFixedSize(64, 32)
        self.m_selectedWidthSpinBox.setRange(1, 150)
        self.m_selectedWidthSpinBox.setValue(1)
        self.m_selectedWidthSpinBox.valueChanged.connect(self.onSelectedWidthSpinBoxEdited)

        # Selected color
        self.m_selectedColorLabel = QColorLabel(QtGui.QColor(QtGui.Qt.GlobalColor.black))
        self.m_selectedColorLabel.setFixedSize(32, 32)
        self.m_selectedColorLabel.mouseLeftButtonClickedSignal.connect(self.onSelectedColorLabelClicked)

        # Default colors
        self.m_defaultColorFirstLineLayout = QtWidgets.QHBoxLayout()
        self.m_defaultColorFirstLineLayout.setSpacing(0)
        self.createDefaultColorsLine(self.m_defaultColorFirstLineLayout, DefaultColorsFirstRow)
        self.m_defaultColorSecondLineLayout = QtWidgets.QHBoxLayout()
        self.m_defaultColorSecondLineLayout.setSpacing(0)
        self.createDefaultColorsLine(self.m_defaultColorSecondLineLayout, DefaultColorsSecondRow)
        self.m_defaultColorsLayout = QtWidgets.QVBoxLayout()
        self.m_defaultColorsLayout.setSpacing(0)
        self.m_defaultColorsLayout.addLayout(self.m_defaultColorFirstLineLayout)
        self.m_defaultColorsLayout.addLayout(self.m_defaultColorSecondLineLayout)

        # Main layout
        self.m_mainLayout = QtWidgets.QHBoxLayout()
        self.m_mainLayout.addStretch()
        self.m_mainLayout.addWidget(self.m_fillPushButton)
        self.m_mainLayout.addWidget(self.m_selectedWidthSpinBox)
        self.m_mainLayout.addWidget(self.m_selectedColorLabel)
        self.m_mainLayout.addLayout(self.m_defaultColorsLayout)
        self.setLayout(self.m_mainLayout)

    def createDefaultColorsLine(self, layout : QtWidgets.QHBoxLayout, colors: list):
        for color in colors:
            label = QColorLabel(color)
            label.setFixedSize(16, 16)
            label.mouseLeftButtonClickedSignal.connect(self.onDefaultColorLabelClicked)
            layout.addWidget(label)

    @QtCore.Slot(QtGui.QColor)
    def onDefaultColorLabelClicked(self):
        colorLabel = self.sender()
        self.selectColor(colorLabel.m_color)  

    @QtCore.Slot()
    def onSelectedColorLabelClicked(self):
        color = QtWidgets.QColorDialog.getColor(self.m_selectedColorLabel.m_color)
        if(color.isValid()):
            self.selectColor(color)

    @QtCore.Slot(QtGui.QColor)
    def onSelectedWidthSpinBoxEdited(self):
        self.onSelectedWidthChangedSignal.emit(self.m_selectedWidthSpinBox.value())

    @QtCore.Slot(QtGui.QColor)
    def selectColor(self, color: QtGui.QColor):
        self.m_selectedColorLabel.updateColor(color)
        self.onSelectedColorChangedSignal.emit(self.m_selectedColorLabel.m_color)

