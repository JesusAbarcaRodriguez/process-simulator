from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from model.process import Process
from util.states import ProcessState
from PyQt5 import QtWidgets

class MainView(QMainWindow):

    def __init__(self):  # this
        super(MainView, self).__init__()
        uic.loadUi("view/view.ui", self)
        self.btn_start.clicked.connect(self.start_process)
        self.btn_stop.clicked.connect(self.stop_process)
        # Verificar si el layout está configurado correctamente
        if self.frame_inferior_izquierdo.layout() is None:
            self.frame_inferior_izquierdo.setLayout(QtWidgets.QVBoxLayout()) # Configurar un QVBoxLayout
    def start_process(self):
        process1 = Process(1, ProcessState.NEW, "Process 1", 1, 10, 0, 0, 5)
        process2 = Process(2, ProcessState.NEW, "Process 2", 2, 5, 0, 0, 5)
        process3 = Process(3, ProcessState.NEW, "Process 3", 3, 15, 0, 0, 5)
        process4 = Process(4, ProcessState.NEW, "Process 4", 4, 7, 0, 0, 5)
        boton1 = QtWidgets.QPushButton(process1.name)
        boton2 = QtWidgets.QPushButton(process2.name)
        boton3 = QtWidgets.QPushButton(process3.name)
        boton4 = QtWidgets.QPushButton(process4.name)

        self.frame_inferior_izquierdo.layout().addWidget(boton1)
        self.frame_inferior_izquierdo.layout().addWidget(boton2)
        self.frame_inferior_izquierdo.layout().addWidget(boton3)
        self.frame_inferior_izquierdo.layout().addWidget(boton4)
    def stop_process(self):
        pass