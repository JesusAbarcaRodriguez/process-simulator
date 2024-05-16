from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from controller.process_controller import suspend_process
from model.process import Process
from util.states import ProcessState
from PyQt5 import QtWidgets
from model.orders import third_order
from PyQt5.QtWidgets import QMessageBox
from view.table.table import create_primary_table, create_secondary_table
from controller.memory_controller import initialize_primary_memory, initialize_secondary_memory
class MainView(QMainWindow):

    def __init__(self):  # this
        super(MainView, self).__init__()
        uic.loadUi("view/view.ui", self)
        self.btn_start.clicked.connect(self.start_process)
        self.btn_stop.clicked.connect(self.stop_process)
        self.btn_sort.clicked.connect(self.sort_process)
        self.btn_assign.clicked.connect(self.assign_process)
        self.btn_add_process.clicked.connect(self.add_process)
        self.btn_suspend.clicked.connect(self.suspend_process_table)
        self.started = False

        create_secondary_table(self)
        create_primary_table(self)
        self.table_memory_principal.itemClicked.connect(self.handle_item_clicked)
        self.selected_process = None
        # Verificar si el layout está configurado correctamente
        if self.frame_inferior1.layout() is None:
            self.frame_inferior1.setLayout(QtWidgets.QVBoxLayout()) # Configurar un QVBoxLayout

    def start_process(self):
        if self.started == False:
            self.pri_mem = initialize_primary_memory(self)
            self.sec_mem = initialize_secondary_memory(self)
            self.add_process_table_secondary(self.sec_mem.block_memory_list)

    def assign_process(self):
        if not self.started:
            QMessageBox.critical(self, "Error", "Debe iniciar el programa primero.")
        else:
            is_assigned = False

            temp = self.pri_mem.assign_memory(
                self.sec_mem.block_memory_list, 
                self.sec_mem
            )

            self.sec_mem.block_memory_list = temp[0]
            self.pri_mem.block_memory_list = temp[1]
            is_assigned = temp[2]
            self.pri_mem = temp[3]
            self.sec_mem = temp[4]

            if is_assigned == False:
                QMessageBox.critical(self, "Error", "No hay bloques de memoria principal libres para asignar procesos.")
            else:
                self.add_process_table_primary(self.pri_mem.block_memory_list)
                self.add_process_table_secondary(self.sec_mem.block_memory_list)

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
                self.sec_mem.block_memory_list = self.sec_mem.assign_proc_to_sec_mem(self.proc)
                self.add_process_table_secondary(self.sec_mem.block_memory_list)
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
        self.table_memory_principal.setRowCount(len(block_primary_list))
        for block in block_primary_list:
            if block.proc is not None:
                self.table_memory_principal.setItem(row, 0, QtWidgets.QTableWidgetItem(str(block.proc.name)))
                self.table_memory_principal.setItem(row, 1, QtWidgets.QTableWidgetItem(str(block.proc.size)))
                self.table_memory_principal.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block.proc.pid)))
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
        for block in self.sec_mem.block_memory_list:
            if block.proc is None:
                return False
        return True
    def handle_item_clicked(self, item):
        id = self.table_memory_principal.item(item.row(), 2).text()
        self.id_process = int(id)
    def suspend_process_table(self):
        suspend_process(self)