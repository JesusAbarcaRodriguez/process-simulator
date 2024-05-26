import threading
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from controller.memory_window_controller import MemoryWindow
from model.page import create_pages
from controller.process_controller import create_process, end_process, suspend_process,assign_suspended_proc_to_pri_mem
from PyQt5 import QtWidgets
from model.orders import third_order
from util.states import ProcessState
from view.table.table import create_primary_table, create_secondary_table
from controller.memory_controller import assign_page_to_pri_mem, initialize_primary_memory, initialize_secondary_memory
from util.message import show_error_message
class MainView(QMainWindow):

    def __init__(self):  # this
        super(MainView, self).__init__()
        uic.loadUi("view/view.ui", self)

        self.btn_start.clicked.connect(self.start_process)
        self.btn_add_process.clicked.connect(self.add_process)
        self.btn_suspend.clicked.connect(self.suspend_process_table)
        self.btn_memory.clicked.connect(self.open_memory_window)
        self.btn_end.clicked.connect(self.end_process_table)
        self.btn_assign.clicked.connect(self.assign_process_to_memory)

        self.started = False
        self.is_item_clicked = False
        self.memory_window = None
        create_secondary_table(self)
        create_primary_table(self)
        self.table_memory_principal.itemClicked.connect(self.handle_item_clicked_pri_mem)
        self.table_memory_secondary.itemClicked.connect(self.handle_item_clicked_sec_mem)
        self.selected_process = None

        # Verificar si el layout está configurado correctamente
        if self.frame_inferior1.layout() is None:
            self.frame_inferior1.setLayout(QtWidgets.QVBoxLayout()) # Configurar un QVBoxLayout

    def start_process(self):
        if self.started == False:
            self.pri_mem = initialize_primary_memory(self)
            self.sec_mem = initialize_secondary_memory(self)
            self.order_print_table_memory()
            thread_pri_memory = threading.Thread(target=self.create_thread_to_pri_memory)
            thread_pri_memory.start()
    def add_process(self):
        if not self.started:
            show_error_message(self, "Error", "Debe iniciar el programa primero.")
        else:
            self.proc = create_process(self)
            if self.pri_mem.is_memory_full_to_process() == False:
                self.pri_mem.block_memory_list = self.pri_mem.assign_proc_to_pri_mem(self.proc)
                time.sleep(1)
                self.order_print_table_memory()
            else:
                self.pri_mem.block_memory_list, self.sec_mem.block_memory_list = create_pages(self) # type: ignore
                self.print_tables()

    def clear_table(self, table):
        table.clearContents()
        table.setRowCount(0)

    def set_table_row_count(self, table, count):
        table.setRowCount(count)

    def add_row_to_table(self, table, row, block):
        if block.is_process:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(block.data.name)))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(block.data.size)))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block.data.pid)))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(block.data.state.value)))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(block.data.priority)))
            table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(block.data.executed_time)))
            table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(block.data.waiting_time)))
            table.setItem(row, 7, QtWidgets.QTableWidgetItem(str(block.data.to_finish_time)))
        else:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(block.data.page_id)))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(block.data.size)))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block.data.page_number)))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(block.data.process.state.value)))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(block.data.process.priority)))
            table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(block.data.executed_time)))
            table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(block.data.waiting_time)))
            table.setItem(row, 7, QtWidgets.QTableWidgetItem(str(block.data.to_finish_time)))

    def add_process_table(self, table, block_primary_list):
        self.clear_table(table)
        if not block_primary_list:
            return
        self.set_table_row_count(table,
                                 len(block_primary_list))
        for row, block in enumerate(block_primary_list):
            if block.data and table == self.table_memory_principal:
                self.add_row_to_table(table, row, block)
            elif block.data and table == self.table_memory_secondary:
                self.add_row_to_table(table, row, block)

    def handle_item_clicked_pri_mem(self, item):
        id = self.table_memory_principal.item(item.row(), 2).text()
        self.id_process = int(id)
        self.is_item_clicked = True
    
    def handle_item_clicked_sec_mem(self, item):
        id = self.table_memory_secondary.item(item.row(), 2).text()
        self.id_process = int(id)
        self.is_item_clicked = True

    def suspend_process_table(self):
        if self.is_item_clicked:
            suspend_process(self)
            self.order_print_table_memory()
        else:
            show_error_message( self, "Error", "Debe seleccionar un proceso de memoria principal para suspenderlo." )
    
    def assign_process_to_memory(self):
        if self.is_item_clicked:
            assign_suspended_proc_to_pri_mem(self)
            self.order_print_table_memory()
        else:
            show_error_message( self, "Error", "Debe seleccionar un proceso de memoria secundaria para asignarlo a la memoria principal.")
    def end_process_table(self):
        if self.is_item_clicked:
            end_process(self)
            self.order_print_table_memory()
        else:
            show_error_message( self,  "Error", "Debe seleccionar un proceso de memoria principal para eliminarlo.")

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
                if block.is_process and block.data is not None:
                    if block.data.executed_time >= block.data.to_finish_time:
                        block.data.terminate()
                        block.data = None
                        self.pri_mem.current_size -= 1
                        if any(block.data is not None for block in self.sec_mem.block_memory_list):
                            self.pri_mem.block_memory_list, self.sec_mem.block_memory_list = assign_page_to_pri_mem(self)
                        self.order_print_table_memory()
                        time.sleep(1)
                    else:
                        if block.data.state == ProcessState.RUNNING:
                            block.data.executed_time += 1
                        else:
                            block.data.waiting_time += 1
            time.sleep(1)
            self.add_process_table(self.table_memory_principal, self.pri_mem.block_memory_list)  # Update the table

    def order_print_table_memory(self):
        self.pri_mem.block_memory_list = third_order(self.pri_mem.block_memory_list)
        self.add_process_table(self.table_memory_principal, self.pri_mem.block_memory_list)
    
    def print_tables(self):
        self.add_process_table(self.table_memory_principal, self.pri_mem.block_memory_list)
        self.add_process_table(self.table_memory_secondary, self.sec_mem.block_memory_list)