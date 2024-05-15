import sys
import random
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from model.block_memory import BlockMemory
from model.memory import Memory
from model.process import Process
from model.process_table import ProcessTable
from util.states import ProcessState
from PyQt5 import QtWidgets
from model.orders import third_order
from PyQt5.QtWidgets import QMessageBox
class MainView(QMainWindow):

    def __init__(self):  # this
        super(MainView, self).__init__()
        uic.loadUi("view/view.ui", self)
        self.btn_start.clicked.connect(self.start_process)
        self.btn_stop.clicked.connect(self.stop_process)
        self.btn_sort.clicked.connect(self.sort_process)
        self.btn_assign.clicked.connect(self.assign_process)
        self.btn_add_process.clicked.connect(self.add_process)
        self.started = False
        self.table_memory_principal.setColumnWidth(0, 100)
        self.table_memory_principal.setColumnWidth(1, 197)
        self.table_memory_principal.setColumnWidth(2, 197)
        self.table_memory_principal.setColumnWidth(3, 197)
        self.table_memory_principal.setColumnWidth(4, 197)
        self.table_memory_principal.setColumnWidth(5, 197)
        self.table_memory_principal.setColumnWidth(6, 120)

        self.table_memory_secondary.setColumnWidth(0, 100)
        self.table_memory_secondary.setColumnWidth(1, 197)
        self.table_memory_secondary.setColumnWidth(2, 197)
        self.table_memory_secondary.setColumnWidth(3, 197)
        self.table_memory_secondary.setColumnWidth(4, 197)
        self.table_memory_secondary.setColumnWidth(5, 197)
        self.table_memory_secondary.setColumnWidth(6, 120)
        # Verificar si el layout está configurado correctamente
        if self.frame_inferior1.layout() is None:
            self.frame_inferior1.setLayout(QtWidgets.QVBoxLayout()) # Configurar un QVBoxLayout

    def start_process(self):
        if self.started == False:
            self.process1 = Process(1, ProcessState.NEW, 200, "Process 1", 1, 0, 0, 0, 0)
            self.process2 = Process(2, ProcessState.NEW, 100, "Process 2", 2, 5, 0, 0, 0)
            self.process3 = Process(3, ProcessState.NEW, 20, "Process 3", 2, 15, 0, 0, 0)
            self.process4 = Process(4, ProcessState.NEW, 40, "Process 4", 1, 7, 0, 0, 0)
            self.num_process = 4
            self.process_list_secondary_memory = [self.process1, self.process2, self.process3, self.process4]

            self.block1_secondary = BlockMemory(1, 100, None)
            self.block2_secondary = BlockMemory(2, 200, None)
            self.block3_secondary = BlockMemory(3, 300, None)
            self.block4_secondary = BlockMemory(4, 400, None)
            self.block5_secondary = BlockMemory(5, 500, None)
            self.block6_secondary = BlockMemory(6, 600, None)
            self.block7_secondary = BlockMemory(7, 700, None)
            self.block8_secondary = BlockMemory(8, 800, None)
            self.block9_secondary = BlockMemory(9, 900, None)
            self.block10_secondary = BlockMemory(10, 1000, None)

            #instance secondary memory
            self.memory_secondary = Memory(9, 0, "Secondary")
            self.memory_secondary.block_memory_list = [self.block1_secondary, self.block2_secondary, self.block3_secondary, self.block4_secondary, self.block5_secondary, self.block6_secondary, self.block7_secondary, self.block8_secondary, self.block9_secondary, self.block10_secondary]
            self.memory_secondary.block_memory_list,self.memory_secondary = self.memory_secondary.assign_memory_secondary(self.process_list_secondary_memory, self.c.block_memory_list,self.memory_secondary)
            self.add_process_table_secondary(self.memory_secondary.block_memory_list)
            self.started = True

            self.block1 = BlockMemory(1, 300, None)
            self.block2 = BlockMemory(2, 400, None)
            self.block3 = BlockMemory(3, 500, None)
            self.block4 = BlockMemory(4, 400, None)
            self.block5 = BlockMemory(5, 500, None)
            #instance primary memory
            self.memory_principal = Memory(4, 0, "Primary")
            self.memory_principal.block_memory_list = [self.block1, self.block2, self.block3, self.block4, self.block5]
    def assign_process(self):
        if not self.started:
            QMessageBox.critical(self, "Error", "Debe iniciar el programa primero.")
        else:
            is_assigned = False
            self.memory_secondary.block_memory_list,self.memory_principal.block_memory_list,is_assigned,self.memory_principal,self.memory_secondary = self.memory_principal.assign_memory(self.memory_secondary.block_memory_list, self.memory_principal.block_memory_list,self.memory_principal,self.memory_secondary)
            if is_assigned == False:
                QMessageBox.critical(self, "Error", "No hay bloques de memoria principal libres para asignar procesos.")
            else:
                self.add_process_table_primary(self.memory_principal.block_memory_list)
                self.add_process_table_secondary(self.memory_secondary.block_memory_list)
    def stop_process(self):
        pass
    def sort_process(self):
        if not self.started:
            QMessageBox.critical(self, "Error", "Debe iniciar el programa primero.")
        else:
            self.process_list = third_order(self.process_list)
            self.add_process_table(self.process_list)
        pass
    def add_process(self):
        if not self.started:
            QMessageBox.critical(self, "Error", "Debe iniciar el programa primero.")
        else:
            self.num_process += 1
            name = f"Process {self.num_process}"
            self.proc = Process(self.num_process, ProcessState.NEW, 100, name, 2, 5, 0, 0, 0)
            if self.is_secondary_memory_full() == False:
                self.memory_secondary.block_memory_list = self.memory_secondary.assign_proc_to_memory_secondary(self.proc, self.memory_secondary.block_memory_list)
                self.add_process_table_secondary(self.memory_secondary.block_memory_list)
            else:
                QMessageBox.critical(self, "Error", "No hay bloques de memoria secundaria libres para agregar el proceso.")
        pass
    def add_process_table_primary(self, block_primary_list):
        self.table_memory_principal.clearContents()
        self.table_memory_principal.setRowCount(0) 
        if not block_primary_list:
            self.table_memory_principal.setRowCount(0)  # Limpiar la tabla si no hay datos
            return  # Salir de la función ya que no hay elementos que mostrar
        row = 0
        self.table_memory_principal.setRowCount(len(block_primary_list))
        row = 0
        self.table_memory_principal.setRowCount(len(block_primary_list))
        for block in block_primary_list:
            if block.proc is not None:
                self.table_memory_principal.setItem(row, 0, QtWidgets.QTableWidgetItem(str(block.proc.name)))
                self.table_memory_principal.setItem(row, 1, QtWidgets.QTableWidgetItem(str(block.proc.size)))
                self.table_memory_principal.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block.proc.to_finish_time)))
                self.table_memory_principal.setItem(row, 3, QtWidgets.QTableWidgetItem(str(block.proc.executed_time)))
                self.table_memory_principal.setItem(row, 4, QtWidgets.QTableWidgetItem(str(block.proc.priority)))
                row += 1
        pass
    def add_process_table_secondary(self, block_secondary_list):
        self.table_memory_secondary.clearContents()
        self.table_memory_secondary.setRowCount(0) 
        if not block_secondary_list:
            self.table_memory_secondary.setRowCount(0)  # Limpiar la tabla si no hay datos
            return  # Salir de la función ya que no hay elementos que mostrar
        row = 0
        self.table_memory_secondary.setRowCount(len(block_secondary_list))
        for block in block_secondary_list:
            if block.proc is not None:
                self.table_memory_secondary.setItem(row, 0, QtWidgets.QTableWidgetItem(str(block.proc.name)))
                self.table_memory_secondary.setItem(row, 1, QtWidgets.QTableWidgetItem(str(block.proc.size)))
                self.table_memory_secondary.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block.proc.to_finish_time)))
                self.table_memory_secondary.setItem(row, 3, QtWidgets.QTableWidgetItem(str(block.proc.executed_time)))
                self.table_memory_secondary.setItem(row, 4, QtWidgets.QTableWidgetItem(str(block.proc.priority)))
                row += 1
    def is_secondary_memory_full(self):
        for block in self.memory_secondary.block_memory_list:
            if block.proc is None:
                return False
        return True
