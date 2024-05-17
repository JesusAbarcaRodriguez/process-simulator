from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from controller.figure_controller import FigureOne
class MemoryWindow(QMainWindow):
    closed = pyqtSignal()
    def __init__(self):
        super(MemoryWindow, self).__init__()
        uic.loadUi("view/memory.ui", self)
        self.figura = FigureOne()
        self.figura2 = FigureOne()
        self.graphic1.addWidget(self.figura)
        self.graphic2.addWidget(self.figura2)

    def closeEvent(self, event):
        # Emitir la señal cuando la ventana se cierra
        self.closed.emit()
        super().closeEvent(event)