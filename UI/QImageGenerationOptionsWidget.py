from PySide6 import QtCore, QtWidgets

from Model.ImageGenerator import PretrainedModelName

class QImageGenerationOptionsWidget(QtWidgets.QWidget):
    onAnyOptionChangedSignal = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Prompt Line & model combo box
        self.m_promptLineEdit = QtWidgets.QLineEdit()
        self.m_promptLineEdit.setPlaceholderText("Example: a photograph of an astronaut riding a horse")
        self.m_promptLineEdit.editingFinished.connect(self.onAnyOptionChangedSignal)
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
        self.m_strengthSpinBox.editingFinished.connect(self.onAnyOptionChangedSignal)
        self.m_numInferenceStepsSpinBox = QtWidgets.QSpinBox()
        self.m_numInferenceStepsSpinBox.setRange(1, 256)
        self.m_numInferenceStepsSpinBox.setValue(20)
        self.m_numInferenceStepsSpinBox.editingFinished.connect(self.onAnyOptionChangedSignal)
        self.m_guidanceScaleDoubleSpinBox = QtWidgets.QDoubleSpinBox()
        self.m_guidanceScaleDoubleSpinBox.setRange(1.0, 10.0)
        self.m_guidanceScaleDoubleSpinBox.setValue(7.5)
        self.m_guidanceScaleDoubleSpinBox.editingFinished.connect(self.onAnyOptionChangedSignal)
        self.m_seedSpinBox = QtWidgets.QSpinBox()
        self.m_seedSpinBox.editingFinished.connect(self.onAnyOptionChangedSignal)
        self.m_generateRandomNumberPushButton = QtWidgets.QPushButton("Generate random seed")
        self.m_generateRandomNumberPushButton.clicked.connect(self.onAnyOptionChangedSignal)

        # Options Layouts
        self.m_seedOptionsLayout = QtWidgets.QHBoxLayout()
        self.m_seedOptionsLayout.addWidget(self.m_seedSpinBox)
        self.m_seedOptionsLayout.addWidget(self.m_generateRandomNumberPushButton)
        self.m_seedGroupBox = QtWidgets.QGroupBox(" Use custom seed ")
        self.m_seedGroupBox.setCheckable(True)
        self.m_seedGroupBox.setChecked(False)
        self.m_seedGroupBox.setLayout(self.m_seedOptionsLayout)

        self.m_strengthLabel = QtWidgets.QLabel("Strength:")
        self.m_numInferenceStepsLabel = QtWidgets.QLabel("Iteration steps:")
        self.m_guidanceScaleLabel = QtWidgets.QLabel("Guidance scale:")
        self.m_standardOptionsLayout = QtWidgets.QGridLayout()
        self.m_standardOptionsLayout.addWidget(self.m_strengthLabel, 0, 0)
        self.m_standardOptionsLayout.addWidget(self.m_strengthSpinBox, 0, 1)
        self.m_standardOptionsLayout.addWidget(self.m_numInferenceStepsLabel, 0, 2)
        self.m_standardOptionsLayout.addWidget(self.m_numInferenceStepsSpinBox, 0, 3)
        self.m_standardOptionsLayout.addWidget(self.m_guidanceScaleLabel, 1, 0)
        self.m_standardOptionsLayout.addWidget(self.m_guidanceScaleDoubleSpinBox, 1, 1)

        self.m_generationOptionsLayout = QtWidgets.QHBoxLayout()
        self.m_generationOptionsLayout.addLayout(self.m_standardOptionsLayout)
        self.m_generationOptionsLayout.addWidget(self.m_seedGroupBox)

        # Main Layout
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addLayout(self.m_promptLayout)
        mainLayout.addLayout(self.m_generationOptionsLayout)
        self.setLayout(mainLayout)
