from PySide6 import QtCore, QtWidgets, QtGui

from Model.ImageGenerator import PretrainedModelName

from UI.QClickableLabel import QClickableLabel
from UI.QGeneratedImageLabel import QGeneratedImageLabel
from UI.Drawing.QPaintWidget import QPaintWidget
from UI.Drawing.QPaintOptionsWidget import QPaintOptionsWidget

class MainWindowUI(QtWidgets.QWidget):
    onAnyParameterChangedSignal = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Prompt Line & model combo box
        self.m_promptLineEdit = QtWidgets.QLineEdit()
        self.m_promptLineEdit.setPlaceholderText("Example: a photograph of an astronaut riding a horse")
        self.m_promptLineEdit.editingFinished.connect(self.onAnyParameterChangedSignal)
        self.m_modelNameComboBox = QtWidgets.QComboBox()
        for model in list(PretrainedModelName):    
            self.m_modelNameComboBox.addItem(model.value, model)
        self.m_promptLayout = QtWidgets.QHBoxLayout()
        self.m_promptLayout.addWidget(self.m_promptLineEdit)
        self.m_promptLayout.addWidget(self.m_modelNameComboBox)

        # Options Widgets        
        self.m_strengthSpinBox = QtWidgets.QDoubleSpinBox()
        self.m_strengthSpinBox.setRange(0.01, 1.0)
        self.m_strengthSpinBox.setSingleStep(0.01)
        self.m_strengthSpinBox.setValue(0.95)
        self.m_strengthSpinBox.editingFinished.connect(self.onAnyParameterChangedSignal)
        self.m_numInferenceStepsSpinBox = QtWidgets.QSpinBox()
        self.m_numInferenceStepsSpinBox.setRange(1, 256)
        self.m_numInferenceStepsSpinBox.setValue(20)
        self.m_numInferenceStepsSpinBox.editingFinished.connect(self.onAnyParameterChangedSignal)
        self.m_guidanceScaleDoubleSpinBox = QtWidgets.QDoubleSpinBox()
        self.m_guidanceScaleDoubleSpinBox.setRange(1.0, 10.0)
        self.m_guidanceScaleDoubleSpinBox.setValue(7.5)
        self.m_guidanceScaleDoubleSpinBox.editingFinished.connect(self.onAnyParameterChangedSignal)
        self.m_seedSpinBox = QtWidgets.QSpinBox()
        self.m_seedSpinBox.editingFinished.connect(self.onAnyParameterChangedSignal)
        self.m_generateRandomNumberPushButton = QtWidgets.QPushButton("Generate random seed")
        self.m_generateRandomNumberPushButton.clicked.connect(self.onAnyParameterChangedSignal)

        # Options Layouts
        self.m_strengthLabel = QtWidgets.QLabel("Strength:")
        self.m_numInferenceStepsLabel = QtWidgets.QLabel("Iteration steps:")
        self.m_guidanceScaleLabel = QtWidgets.QLabel("Guidance scale:")
        self.m_standardOptionsLayout = QtWidgets.QGridLayout()
        self.m_standardOptionsLayout.addWidget(self.m_strengthLabel, 1, 0)
        self.m_standardOptionsLayout.addWidget(self.m_strengthSpinBox, 1, 1)
        self.m_standardOptionsLayout.addWidget(self.m_numInferenceStepsLabel, 1, 2)
        self.m_standardOptionsLayout.addWidget(self.m_numInferenceStepsSpinBox, 1, 3)
        self.m_standardOptionsLayout.addWidget(self.m_guidanceScaleLabel, 1, 4)
        self.m_standardOptionsLayout.addWidget(self.m_guidanceScaleDoubleSpinBox, 1, 5)

        self.m_seedOptionsLayout = QtWidgets.QHBoxLayout()
        self.m_seedOptionsLayout.addWidget(self.m_seedSpinBox)
        self.m_seedOptionsLayout.addWidget(self.m_generateRandomNumberPushButton)
        self.m_seedGroupBox = QtWidgets.QGroupBox(" Use custom seed ")
        self.m_seedGroupBox.setCheckable(True)
        self.m_seedGroupBox.setChecked(False)
        self.m_seedGroupBox.setLayout(self.m_seedOptionsLayout)

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
        mainLayout.addLayout(self.m_promptLayout)
        mainLayout.addLayout(self.m_standardOptionsLayout)
        mainLayout.addWidget(self.m_seedGroupBox)
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
        