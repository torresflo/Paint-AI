import io
from random import Random

from PySide6 import QtCore, QtWidgets, QtGui
from PIL.ImageQt import ImageQt
from PIL import Image

from Model.ImageGenerator import ImageGenerator, PretrainedModelName

from UI.QClickableLabel import QClickableLabel
from UI.QGeneratedImageLabel import QGeneratedImageLabel
from UI.QPaintWidget import QPaintWidget

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_maxRandomNumber = 1000000000
        self.randomNumberGenerator = Random()

        #Model
        self.m_imageGenerator = ImageGenerator()

        # Prompt Line & model combo box
        self.m_promptLineEdit = QtWidgets.QLineEdit()
        self.m_promptLineEdit.setPlaceholderText("Example: a photograph of an astronaut riding a horse")
        self.m_modelNameComboBox = QtWidgets.QComboBox()
        for model in list(PretrainedModelName):    
            self.m_modelNameComboBox.addItem(model.value, model)
        self.m_promptLayout = QtWidgets.QHBoxLayout()
        self.m_promptLayout.addWidget(self.m_promptLineEdit)
        self.m_promptLayout.addWidget(self.m_modelNameComboBox)

        # Options Widgets        
        self.m_strengthSpinBox = QtWidgets.QDoubleSpinBox()
        self.m_strengthSpinBox.setRange(0.0, 1.0)
        self.m_strengthSpinBox.setValue(0.75)
        self.m_numInferenceStepsSpinBox = QtWidgets.QSpinBox()
        self.m_numInferenceStepsSpinBox.setRange(1, 256)
        self.m_numInferenceStepsSpinBox.setValue(10)
        self.m_guidanceScaleDoubleSpinBox = QtWidgets.QDoubleSpinBox()
        self.m_guidanceScaleDoubleSpinBox.setRange(1.0, 10.0)
        self.m_guidanceScaleDoubleSpinBox.setValue(7.5)
        self.m_seedSpinBox = QtWidgets.QSpinBox()
        self.m_seedSpinBox.setRange(0, self.m_maxRandomNumber)
        self.m_seedSpinBox.setValue(self.generateRandomNumber())
        self.m_generateRandomNumberPushButton = QtWidgets.QPushButton("Generate random seed")
        self.m_generateRandomNumberPushButton.clicked.connect(self.onGenerateRandomNumberPushButtonClicked)

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

        # Generate Button
        self.m_generateImagePushButton = QtWidgets.QPushButton("Generate image")
        self.m_generateImagePushButton.clicked.connect(self.onGenerateImagePushButtonClicked)

        # Image Label
        self.m_resultImageLabel = QGeneratedImageLabel()
        self.m_paintWidget = QPaintWidget()

        # Image Layout
        self.m_imageLayout = QtWidgets.QHBoxLayout()
        self.m_imageLayout.addWidget(self.m_resultImageLabel)
        self.m_imageLayout.addWidget(self.m_paintWidget)

        # Drawing options
        self.m_penWidthSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.m_penWidthSlider.setMaximumWidth(100)
        self.m_penWidthSlider.setMaximum(100)
        self.m_penWidthSlider.setValue(self.m_paintWidget.m_penWidth)
        self.m_penWidthSlider.valueChanged.connect(self.onPenWidthSliderValueChanged)
        self.m_penColorLabel = QClickableLabel()
        self.m_penColorLabel.setFixedSize(30, 30)
        self.m_penColorLabel.mouseLeftButtonClickedSignal.connect(self.onPenColorLabelClicked)
        self.updatePenColorLabel()
        self.m_fillPushButton = QtWidgets.QPushButton("Fill")
        self.m_fillPushButton.setCheckable(True)

        # Drawing options layout
        self.m_drawingOptionsLayout = QtWidgets.QHBoxLayout()
        self.m_drawingOptionsLayout.addStretch()
        self.m_drawingOptionsLayout.addWidget(self.m_penWidthSlider)
        self.m_drawingOptionsLayout.addWidget(self.m_penColorLabel)
        self.m_drawingOptionsLayout.addWidget(self.m_fillPushButton)
        self.m_drawingOptionsLayout.addStretch()

        # Main Layout
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addLayout(self.m_promptLayout)
        mainLayout.addLayout(self.m_standardOptionsLayout)
        mainLayout.addWidget(self.m_seedGroupBox)
        mainLayout.addWidget(self.m_generateImagePushButton)
        mainLayout.addLayout(self.m_imageLayout)
        mainLayout.addLayout(self.m_drawingOptionsLayout)
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.setLayout(mainLayout)

    def updatePenColorLabel(self):
        palette = self.m_penColorLabel.palette()
        palette.setColor(self.m_penColorLabel.backgroundRole(), self.m_paintWidget.m_penColor)
        self.m_penColorLabel.setAutoFillBackground(True)
        self.m_penColorLabel.setPalette(palette)

    def generateRandomNumber(self):
        return self.randomNumberGenerator.randint(0, self.m_maxRandomNumber)

    @QtCore.Slot()
    def onGenerateRandomNumberPushButtonClicked(self):
        self.m_seedSpinBox.setValue(self.generateRandomNumber())

    @QtCore.Slot()
    def onGenerateImagePushButtonClicked(self):
        promptString = self.m_promptLineEdit.text()
        if promptString:
            width = 512
            height = 512
            numInferenceSteps = self.m_numInferenceStepsSpinBox.value()
            guidanceScale = self.m_guidanceScaleDoubleSpinBox.value()
            strenght = self.m_strengthSpinBox.value()

            seed = self.generateRandomNumber()
            if self.m_seedGroupBox.isChecked():
                seed = self.m_seedSpinBox.value()
            else:
                self.m_seedSpinBox.setValue(seed)

            self.m_resultImageLabel.loadWaitingImage(width, height)
            self.repaint()
            QtWidgets.QApplication.processEvents()

            buffer = QtCore.QBuffer()
            buffer.open(QtCore.QBuffer.OpenModeFlag.ReadWrite)
            self.m_paintWidget.m_drawImage.save(buffer, "PNG")
            initImage = Image.open(io.BytesIO(buffer.data()))
            buffer.close()

            model = self.m_modelNameComboBox.currentData()
            image = self.m_imageGenerator.generateImage(modelName=model, prompt=promptString, image=initImage, 
                                                        numInferenceSteps=numInferenceSteps, guidanceScale=guidanceScale, strength=strenght, seed=seed)
            imageQt = ImageQt(image)
            self.m_resultImageLabel.setPixmap(QtGui.QPixmap.fromImage(imageQt))

    @QtCore.Slot()
    def onPenWidthSliderValueChanged(self):
        width = self.m_penWidthSlider.value()
        self.m_paintWidget.m_penWidth = width

    @QtCore.Slot()
    def onPenColorLabelClicked(self):
        color = QtWidgets.QColorDialog.getColor(self.m_paintWidget.m_penColor)
        if(color.isValid()):
            self.m_paintWidget.m_penColor = color
            self.updatePenColorLabel()
        