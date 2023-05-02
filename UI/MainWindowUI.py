from PySide6 import QtCore, QtWidgets, QtGui

from Model.ImageGenerator import PretrainedModelName

from UI.QImageGenerationOptionsWidget import QImageGenerationOptionsWidget
from UI.QGeneratedImageLabel import QGeneratedImageLabel
from UI.Drawing.QPaintWidget import QPaintWidget
from UI.Drawing.QPaintOptionsWidget import QPaintOptionsWidget

class MainWindowUI(QtWidgets.QWidget):
    onAnyParameterChangedSignal = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Generation Options
        self.m_generationOptionsWidget = QImageGenerationOptionsWidget()
        self.m_generationOptionsWidget.onAnyOptionChangedSignal.connect(self.onAnyParameterChangedSignal)

        # Image Label
        self.m_resultImageLabel = QGeneratedImageLabel()
        self.m_paintWidget = QPaintWidget()
        self.m_paintWidget.onDrawImageChanged.connect(self.onAnyParameterChangedSignal)

        # Image Layout
        self.m_imageLayout = QtWidgets.QHBoxLayout()
        self.m_imageLayout.addWidget(self.m_resultImageLabel)
        self.m_imageLayout.addWidget(self.m_paintWidget)

        # Drawing options
        self.m_paintOptionsWidget = QPaintOptionsWidget()
        self.m_paintOptionsWidget.onSelectedFillModeChangedSignal.connect(self.m_paintWidget.setFillMode)
        self.m_paintOptionsWidget.onSelectedWidthChangedSignal.connect(self.m_paintWidget.setPenWidth)
        self.m_paintOptionsWidget.onSelectedColorChangedSignal.connect(self.m_paintWidget.setPenColor)

        # Drawing options layout
        self.m_drawingOptionsLayout = QtWidgets.QHBoxLayout()
        self.m_drawingOptionsLayout.addStretch()
        self.m_drawingOptionsLayout.addWidget(self.m_paintOptionsWidget)
        self.m_drawingOptionsLayout.addStretch()

        # Main Layout
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.m_generationOptionsWidget)
        mainLayout.addLayout(self.m_imageLayout)
        mainLayout.addLayout(self.m_drawingOptionsLayout)
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.setLayout(mainLayout)

        # Undo actions
        self.m_undoAction = QtGui.QAction("Undo", self)
        self.m_undoAction.setShortcut(QtGui.QKeySequence.StandardKey.Undo)
        self.m_undoAction.setShortcutContext(QtGui.Qt.ShortcutContext.ApplicationShortcut)
        self.m_undoAction.triggered.connect(self.m_paintWidget.m_undoStack.undo)
        self.addAction(self.m_undoAction)
        self.m_redoAction = QtGui.QAction("Redo", self)
        self.m_redoAction.setShortcut(QtGui.QKeySequence.StandardKey.Redo)
        self.m_redoAction.setShortcutContext(QtGui.Qt.ShortcutContext.ApplicationShortcut)
        self.m_redoAction.triggered.connect(self.m_paintWidget.m_undoStack.redo)
        self.addAction(self.m_redoAction)
        self.m_paintWidget.setFocus()

    @QtCore.Slot()
    def onPenWidthSliderValueChanged(self):
        width = self.m_penWidthSlider.value()
        self.m_paintWidget.m_penWidth = width
        