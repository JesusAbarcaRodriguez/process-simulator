import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from model.process import Process
from util.states import ProcessState
from PyQt5 import QtWidgets


class MainView(QMainWindow):

    def __init__(self):  # this
        super(MainView, self).__init__()
        uic.loadUi("view/view.ui", self)
        self.btn_start.clicked.connect(self.add_process_table)
        self.btn_stop.clicked.connect(self.stop_process)
        self.table_process.setColumnWidth(0, 100)
        self.table_process.setColumnWidth(1, 197)
        self.table_process.setColumnWidth(2, 197)
        self.table_process.setColumnWidth(3, 197)
    
        # Verificar si el layout está configurado correctamente
        self.add_process_table()
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
    def add_process_table(self ):
        process = [{"Proceso": "Proceso_1", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2},
                   {"Proceso": "Proceso_2", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2},
                   {"Proceso": "Proceso_3", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2},
                   {"Proceso": "Proceso_4", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2},
                   {"Proceso": "Proceso_5", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2},
                   {"Proceso": "Proceso_6", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2},
                   {"Proceso": "Proceso_7", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2},
                   {"Proceso": "Proceso_8", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2},
                   {"Proceso": "Proceso_9", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2},
                   {"Proceso": "Proceso_10", "TiempoEsperando": 100, "TiempoTotalTerminar": 200, "TiempoEjecutado": 300, "Prioridad": 2}]
        
        row = 0
        self.table_process.setRowCount(len(process))
        for pro in process:
            self.table_process.setItem(row, 0, QtWidgets.QTableWidgetItem(pro["Proceso"]))
            self.table_process.setItem(row, 1, QtWidgets.QTableWidgetItem(str(pro["TiempoEsperando"])))
            self.table_process.setItem(row, 2, QtWidgets.QTableWidgetItem(str(pro["TiempoTotalTerminar"])))
            self.table_process.setItem(row, 3, QtWidgets.QTableWidgetItem(str(pro["TiempoEjecutado"])))
            self.table_process.setItem(row, 4, QtWidgets.QTableWidgetItem(str(pro["Prioridad"])))
            row += 1
        pass