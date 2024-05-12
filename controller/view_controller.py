import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from model.process import Process
from util.states import ProcessState
from PyQt5 import QtWidgets
from model.orders import third_order


class MainView(QMainWindow):

    process1 = Process(1, ProcessState.NEW, "Process 1", 1, 10, 0, 0, 5)
    process2 = Process(2, ProcessState.NEW, "Process 2", 2, 5, 0, 0, 5)
    process3 = Process(3, ProcessState.NEW, "Process 3", 2, 15, 0, 0, 5)
    process4 = Process(4, ProcessState.NEW, "Process 4", 1, 7, 0, 0, 5)
        
    process_list = [process1, process2, process3, process4]
        
    def __init__(self):  # this
        super(MainView, self).__init__()
        uic.loadUi("view/view.ui", self)
        self.btn_start.clicked.connect(self.add_process_table)
        self.btn_stop.clicked.connect(self.stop_process)
        self.btn_sort.clicked.connect(self.sort_process)
        
        self.table_process.setColumnWidth(0, 100)
        self.table_process.setColumnWidth(1, 197)
        self.table_process.setColumnWidth(2, 197)
        self.table_process.setColumnWidth(3, 197)
    
        # Verificar si el layout está configurado correctamente
        self.add_process_table(self.process_list)
        if self.frame_inferior_izquierdo.layout() is None:
            self.frame_inferior_izquierdo.setLayout(QtWidgets.QVBoxLayout()) # Configurar un QVBoxLayout
    def start_process(self):
        pass
    def stop_process(self):
        pass
    
    def sort_process(self):
        self.process_list = third_order(self.process_list)
        self.add_process_table(self.process_list)
        
        pass
    
    def add_process_table(self, process_list):
        
        row = 0
        self.table_process.setRowCount(len(process_list))
        for pro in process_list:
            self.table_process.setItem(row, 0, QtWidgets.QTableWidgetItem(str(pro.name)))
            self.table_process.setItem(row, 1, QtWidgets.QTableWidgetItem(str(pro.waiting_time)))
            self.table_process.setItem(row, 2, QtWidgets.QTableWidgetItem(str(pro.to_finish_time)))
            self.table_process.setItem(row, 3, QtWidgets.QTableWidgetItem(str(pro.executed_time)))
            self.table_process.setItem(row, 4, QtWidgets.QTableWidgetItem(str(pro.priority)))
            
            row += 1
        pass