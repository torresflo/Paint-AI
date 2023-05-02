import io
from random import Random

from PySide6 import QtCore, QtGui
from PIL.ImageQt import ImageQt
from PIL import Image

from Model.ImageGenerator import ImageGenerator
from Model.ImageGeneratorWorker import ImageGeneratorWorker

from UI.MainWindowUI import MainWindowUI

class MainWindow(MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_threadpool = QtCore.QThreadPool()
        self.m_generationInProgress = False
        self.m_hasAnyParameterChanged = False

        self.m_maxRandomNumber = 1000000000
        self.randomNumberGenerator = Random()

        # Model
        self.m_imageGenerator = ImageGenerator()

        # Seed
        self.m_generationOptionsWidget.m_seedSpinBox.setRange(0, self.m_maxRandomNumber)
        self.m_generationOptionsWidget.m_seedSpinBox.setValue(self.generateRandomNumber())

        # Connections
        self.m_generationOptionsWidget.m_generateRandomNumberPushButton.clicked.connect(self.onGenerateRandomNumberPushButtonClicked)
        self.onAnyParameterChangedSignal.connect(self.onAnyParameterChanged)

    def generateRandomNumber(self):
        return self.randomNumberGenerator.randint(0, self.m_maxRandomNumber)

    @QtCore.Slot()
    def onGenerateRandomNumberPushButtonClicked(self):
        self.m_generationOptionsWidget.m_seedSpinBox.setValue(self.generateRandomNumber())

    @QtCore.Slot()
    def onAnyParameterChanged(self):
        if(self.m_generationInProgress == False) :
            self.startImageGeneration()
        else :
            self.m_hasAnyParameterChanged = True

    @QtCore.Slot(ImageQt)
    def onImageGenerated(self, image : ImageQt):
        self.m_generationInProgress = False
        self.m_resultImageLabel.setPixmap(QtGui.QPixmap.fromImage(image))

        if(self.m_hasAnyParameterChanged):
            self.m_hasAnyParameterChanged = False
            self.startImageGeneration()

    @QtCore.Slot()
    def startImageGeneration(self):
        promptString = self.m_generationOptionsWidget.m_promptLineEdit.text()
        if promptString:
            self.m_generationInProgress = True

            numInferenceSteps = self.m_generationOptionsWidget.m_numInferenceStepsSpinBox.value()
            guidanceScale = self.m_generationOptionsWidget.m_guidanceScaleDoubleSpinBox.value()
            strenght = self.m_generationOptionsWidget.m_strengthSpinBox.value()

            seed = self.generateRandomNumber()
            if self.m_generationOptionsWidget.m_seedGroupBox.isChecked():
                seed = self.m_generationOptionsWidget.m_seedSpinBox.value()
            else:
                self.m_generationOptionsWidget.m_seedSpinBox.setValue(seed)

            buffer = QtCore.QBuffer()
            buffer.open(QtCore.QBuffer.OpenModeFlag.ReadWrite)
            self.m_paintWidget.m_drawImage.save(buffer, "PNG")
            initImage = Image.open(io.BytesIO(buffer.data()))
            buffer.close()

            model = self.m_generationOptionsWidget.m_modelNameComboBox.currentData()
            
            worker = ImageGeneratorWorker(self.m_imageGenerator, modelName=model, prompt=promptString, image=initImage, 
                                                        numInferenceSteps=numInferenceSteps, guidanceScale=guidanceScale, strength=strenght, seed=seed)
            worker.signals.onImageGeneratedSignal.connect(self.onImageGenerated)
            self.m_threadpool.start(worker)
        