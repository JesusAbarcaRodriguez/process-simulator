import random
import threading
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from controller.figure_controller import FigureOne
from controller.memory_window_controller import MemoryWindow
from controller.process_controller import end_process, suspend_process
from model.process import Process
from util.states import ProcessState
from PyQt5 import QtWidgets
from model.orders import third_order
from PyQt5.QtWidgets import QMessageBox
from view.table.table import create_primary_table, create_secondary_table
from controller.memory_controller import initialize_primary_memory, initialize_secondary_memory
from util.message import show_error_message
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
        self.btn_memory.clicked.connect(self.open_memory_window)
        self.btn_end.clicked.connect(self.end_process_table)

        self.started = False
        self.is_item_clicked = False
        self.memory_window = None
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
            self.add_process_table(self.table_memory_principal, self.pri_mem.block_memory_list)
            thread_pri_memory = threading.Thread(target=self.create_thread_to_pri_memory)
            thread_pri_memory.start()
    def assign_process(self):
        pass
    def stop_process(self):
        pass

    def sort_process(self):
        if not self.started:
            show_error_message(self, "Error", "Debe iniciar el programa primero.")
        else:
            self.process_list = third_order(self.process_list)
            self.add_process_table(self.process_list)
        pass

    def add_process(self):
        if not self.started:
            show_error_message(self, "Error", "Debe iniciar el programa primero.")
        else:
            self.num_process += 1
            name = f"Process {self.num_process}"
            to_finish_time_rand = random.randint(20, 50)
            priority_rand = random.randint(1, 10)
            self.proc = Process(self.num_process, ProcessState.NEW, 100, name, priority_rand, 0, 0, to_finish_time_rand)
            if self.is_primary_memory_full() == False:
                self.pri_mem.block_memory_list = self.pri_mem.assign_proc_to_pri_mem(self.proc)
                self.add_process_table(self.table_memory_principal,self.pri_mem.block_memory_list)
            else:
                show_error_message(
                    self, 
                    "Error", 
                    "No hay bloques de memoria principal libres para agregar el proceso."
                )

    def clear_table(self, table):
        table.clearContents()
        table.setRowCount(0)

    def set_table_row_count(self, table, count):
        table.setRowCount(count)

    def add_row_to_table(self, table, row, block):
        table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(block.proc.name)))
        table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(block.proc.size)))
        table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block.proc.pid)))
        table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(block.proc.state.value)))
        table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(block.proc.priority)))
        table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(block.proc.executed_time)))
        table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(block.proc.waiting_time)))
        table.setItem(row, 7, QtWidgets.QTableWidgetItem(str(block.proc.to_finish_time)))

    def add_process_table(self, table, block_primary_list):
        self.clear_table(table)
        if not block_primary_list:
            return  # Exit the function as there are no items to display
        self.set_table_row_count(table,
                                 len(block_primary_list))
        for row, block in enumerate(block_primary_list):
            if block.proc and table == self.table_memory_principal:
                self.add_row_to_table(table, row, block)
                block.proc.admit()
            elif block.proc and table == self.table_memory_secondary:
                self.add_row_to_table(table, row, block)

    def is_primary_memory_full(self):
        for block in self.pri_mem.block_memory_list:
            if block.proc is None:
                return False
        return True

    def handle_item_clicked(self, item):
        id = self.table_memory_principal.item(item.row(), 2).text()
        self.id_process = int(id)
        self.is_item_clicked = True

    def suspend_process_table(self):
        if self.is_item_clicked:
            suspend_process(self)
        else:
            show_error_message(
                self, 
                "Error",
                "Debe seleccionar un proceso de memoria principal para suspenderlo."
            ) 

    def end_process_table(self):
        if self.is_item_clicked:
            end_process(self)
        else:
            show_error_message(
                self, 
                "Error", 
                "Debe seleccionar un proceso de memoria principal para eliminarlo."
            )

    def open_memory_window(self):
        if not self.memory_window:  # Verificar si la ventana ya está abierta
            self.memory_window = MemoryWindow()
            self.memory_window.show()
            self.memory_window.closed.connect(self.on_memory_window_closed)

    def on_memory_window_closed(self):
        self.memory_window = None  # Restablece la referencia a None

    def create_thread_to_pri_memory(self):
        while True:
            for block in self.pri_mem.block_memory_list:
                if block.proc and block.proc.executed_time >= block.proc.to_finish_time:
                    block.proc.state = ProcessState.TERMINATED
                    block.proc = None
                if block.proc is not None:
                    block.proc.executed_time += 1
            time.sleep(1)
            self.add_process_table(self.table_memory_principal, 
                                self.pri_mem.block_memory_list) 

    def create_thread_to_sec_memory(self):
        while True:
            time.sleep(1)
            for block in self.sec_mem.block_memory_list:
                if block.proc:
                    block.proc.waiting_time += 1 
            self.add_process_table(self.table_memory_secondary, self.sec_mem.block_memory_list)