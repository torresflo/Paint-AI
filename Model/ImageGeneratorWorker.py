from PySide6 import QtCore
from PIL.ImageQt import ImageQt

from Model.ImageGenerator import ImageGenerator, PretrainedModelName

class ImageGeneratorWorkerSignals(QtCore.QObject):
    onImageGeneratedSignal = QtCore.Signal(ImageQt)

class ImageGeneratorWorker(QtCore.QRunnable):

    def __init__(self, imageGenerator : ImageGenerator, modelName : PretrainedModelName, prompt, image, numInferenceSteps, guidanceScale, strength, seed) -> None:
        super().__init__()
        self.signals = ImageGeneratorWorkerSignals()

        self.m_imageGenerator = imageGenerator
        self.m_modelName = modelName
        self.m_prompt = prompt
        self.m_image = image
        self.m_numInferenceSteps = numInferenceSteps
        self.m_guidanceScale = guidanceScale
        self.m_strength = strength
        self.m_seed = seed

    QtCore.Slot()
    def run(self) -> None:
        self.generateImage()

    def generateImage(self):
        image = self.m_imageGenerator.generateImage(self.m_modelName, self.m_prompt, self.m_image, self.m_numInferenceSteps, self.m_guidanceScale, self.m_strength, self.m_seed)
        self.signals.onImageGeneratedSignal.emit(ImageQt(image))
