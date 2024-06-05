from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from controller.figure_controller import FigureOne
class MemoryWindow(QMainWindow):
    closed = pyqtSignal()
    def __init__(self):
        super(MemoryWindow, self).__init__()
        uic.loadUi("view/memory.ui", self)
        is_pri_mem = True

        self.figure_prim_memory = FigureOne(is_pri_mem)
        self.figure_sec_memory = FigureOne(is_pri_mem = False)

        self.graphic1.addWidget(self.figure_sec_memory)
        self.graphic2.addWidget(self.figure_prim_memory)

    def closeEvent(self, event):
        # Emitir la señal cuando la ventana se cierra
        self.closed.emit()
        super().closeEvent(event)