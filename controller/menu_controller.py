import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from controller.view_controller import MainView
from PyQt5.QtCore import pyqtSignal
from util.global_state import GlobalState 
class MenuApp(QtWidgets.QMainWindow):
    closed = pyqtSignal()
    def __init__(self):
        super(MenuApp, self).__init__()
        uic.loadUi('view/menu.ui', self)  # Asegúrate de que el archivo .ui se llame 'memory_config.ui'
        self.button_validate.clicked.connect(self.validate_input)
        self.main_view = None
        self.global_state = GlobalState()
    def validate_input(self):
        self.global_state.set_pri_mem_size(self.spinbox_main_memory.value())
        self.global_state.set_sec_mem_size(self.spinbox_secondary_memory.value())
        self.global_state.set_initial_processes(self.spinbox_initial_processes.value())

        if self.global_state.initial_processes < self.global_state.pri_mem_size and self.global_state.initial_processes < self.global_state.sec_mem_size:
            QMessageBox.information(self, "Validación", "Los valores son válidos")
            self.close()
            self.main_view = MainView()
            self.main_view.show()
        else:
            QMessageBox.warning(self, "Error de Validación", "La cantidad de procesos iniciales debe ser menor a las cantidades de memoria")

    def closeEvent(self, event):
        # Emitir la señal cuando la ventana se cierra
        self.closed.emit()
        super().closeEvent(event)