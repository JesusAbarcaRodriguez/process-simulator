import threading
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from controller.memory_window_controller import MemoryWindow
from model.page import create_pages
from controller.process_controller import create_process, end_process, suspend_process,assign_suspended_proc_to_pri_mem
from PyQt5 import QtWidgets
from util.sorts import first_order, second_order, third_order
from util.states import ProcessState
from view.table.table import create_primary_table, create_secondary_table
from controller.memory_controller import assign_page_to_pri_mem, initialize_primary_memory, initialize_secondary_memory
from util.message import show_error_message
from util.global_state import GlobalState
from PyQt5 import QtWidgets, QtGui
class MainView(QMainWindow):

    def __init__(self):  # this
        super(MainView, self).__init__()
        uic.loadUi("view/view.ui", self)

        self.btn_start.clicked.connect(self.start_process)
        self.btn_stop.clicked.connect(self.closeEvent)
        self.btn_add_process.clicked.connect(self.add_process)
        self.btn_suspend.clicked.connect(self.suspend_process_table)
        self.btn_memory.clicked.connect(self.open_memory_window)
        self.btn_end.clicked.connect(self.end_process_table)
        self.btn_assign.clicked.connect(self.assign_process_to_memory)
        self.box_sort.currentIndexChanged.connect(self.print_sorted_tables)
        self.btn_service.clicked.connect(self.add_service)

        self.started = False
        self.is_item_clicked = False
        self.memory_window = None
        self.num_process = 1
        self.selected_process = None
        self.global_state = GlobalState()
        self.process_aux = None

        create_secondary_table(self)
        create_primary_table(self)

        self.table_memory_principal.itemClicked.connect(self.handle_item_clicked_pri_mem)
        self.table_memory_secondary.itemClicked.connect(self.handle_item_clicked_sec_mem)

        # Verificar si el layout está configurado correctamente
        if self.frame_inferior1.layout() is None:
            self.frame_inferior1.setLayout(QtWidgets.QVBoxLayout()) # Configurar un QVBoxLayout

    def closeEvent(self, event):
        self.close()

    def start_process(self):
        self.pri_mem = initialize_primary_memory(self, self.global_state.get_pri_mem_size(), self.global_state.get_initial_processes())
        self.sec_mem = initialize_secondary_memory(self, self.global_state.get_sec_mem_size())
        self.label_total_pri_mem.setText(str(self.global_state.get_block_prim_memory_size())+" bytes")
        self.label_total_sec_mem.setText(str(self.global_state.get_block_sec_memory_size())+" bytes")
        self.print_sorted_tables()
        self.calculate_global_prim_mem_used()
        thread_pri_memory = threading.Thread(target=self.create_thread_to_pri_memory)
        thread_pri_memory.start()
    
    def add_service(self):
        if not self.started:
            show_error_message(self, "Error", "Debe iniciar el programa primero.")
        else:
            self.service = create_process(self,False)
            if self.pri_mem.is_memory_full_to_process() == False:
                self.pri_mem.block_memory_list,is_assigned = self.pri_mem.assign_proc_to_pri_mem(self.service)
                if not is_assigned:
                    show_error_message(self, "Error", "No hay un bloque de memoria con el tamaño suficiente para asignar el proceso" + " El tamaño del proceso entrante es de " + str(self.service.size))
                time.sleep(1)
            else:
                show_error_message(self, "Error", "No hay suficiente memoria principal para asignar el servicio.")
            self.print_sorted_tables()
    def add_process(self):
        if not self.started:
            show_error_message(self, "Error", "Debe iniciar el programa primero.")
        else:
            self.process_aux = create_process(self,True)
            if self.pri_mem.is_memory_full_to_process() == False:
                self.pri_mem.block_memory_list, is_assigned = self.pri_mem.assign_proc_to_pri_mem(self.process_aux)
                self.calculate_global_prim_mem_used()
                if not is_assigned:
                    show_error_message(self, "Error", "No hay un bloque de memoria con el tamaño suficiente para asignar el proceso" + " El tamaño del proceso entrante es de " + str(self.process_aux.size))
                time.sleep(1)
            else:
                self.pri_mem.block_memory_list, self.sec_mem.block_memory_list = create_pages(self)
                self.print_tables()
                self.calculate_global_sec_mem_used()
                time.sleep(1)
            self.process_aux = None
            self.print_sorted_tables()

    def clear_table(self, table):
        table.clearContents()
        table.setRowCount(0)

    def set_table_row_count(self, table, count):
        table.setRowCount(count)

    def add_row_to_table(self, table, row, block):
        if block.is_process:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(block.block_id) + "/" + str(block.size)))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(block.data.name)))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block.data.size)))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(block.data.pid)))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(block.data.state.value)))
            table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(block.data.priority)))
            table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(block.data.executed_time)))
            table.setItem(row, 7, QtWidgets.QTableWidgetItem(str(block.data.waiting_time)))
            table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(block.data.to_finish_time)))
        else:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(block.block_id) + "/" + str(block.size)))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(block.data.page_id)))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block.data.size)))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(block.data.page_number)))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(block.data.process.state.value)))
            table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(block.data.process.priority)))
            table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(block.data.executed_time)))
            table.setItem(row, 7, QtWidgets.QTableWidgetItem(str(block.data.waiting_time)))
            table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(block.data.to_finish_time)))
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item is not None:
                color = QtGui.QColor(0, 0, 0)
                if block.data.state == ProcessState.TERMINATED:
                    color = QtGui.QColor(255, 0, 0)  # Color rojo para procesos terminados
                elif block.data.state == ProcessState.SUSPENDED_BLOCKED:
                    color = QtGui.QColor(255, 165, 0)   
                elif block.is_process:
                    color = QtGui.QColor(0, 0, 139)  # Color azul para procesos
                else:
                    color = QtGui.QColor(0, 100, 0)  # Color verde para páginas
                item.setForeground(color)

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
            self.print_sorted_tables()
            self.calculate_global_sec_mem_used()
        else:
            show_error_message( self, "Error", "Debe seleccionar un proceso de memoria principal para suspenderlo." )
    
    def assign_process_to_memory(self):
        if self.is_item_clicked:
            assign_suspended_proc_to_pri_mem(self)
            self.print_sorted_tables()
            self.calculate_global_sec_mem_used()
        else:
            show_error_message( self, "Error", "Debe seleccionar un proceso de memoria secundaria para asignarlo a la memoria principal.")
    def end_process_table(self):
        if self.is_item_clicked:
            end_process(self)
            self.print_sorted_tables()
            self.calculate_global_prim_mem_used()
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
                if block.data is not None:
                    if block.data.executed_time >= block.data.to_finish_time:
                        block.data.terminate()
                        self.add_process_table(self.table_memory_principal, self.pri_mem.block_memory_list)  # Update the table
                        time.sleep(1)
                        block.data = None
                        self.calculate_global_prim_mem_used()
                        self.pri_mem.current_size -= 1
                        if any(block.data is not None for block in self.sec_mem.block_memory_list):
                            self.pri_mem.block_memory_list, self.sec_mem.block_memory_list = assign_page_to_pri_mem(self)
                        self.print_tables()
                        self.calculate_global_sec_mem_used()
                        self.print_sorted_tables()
                    else:
                        if block.data.is_running == False:
                            block.data.admit()
                        self.add_process_table(self.table_memory_principal, self.pri_mem.block_memory_list)  # Update the table
            time.sleep(1)
    def print_sorted_tables(self):
        if not self.started:
            show_error_message(self, "Error", "Debe iniciar el programa primero.")
        else:
            box_value = self.box_sort.currentText()
            if box_value == "El tiempo restante más corto":
                self.pri_mem.block_memory_list = first_order(self.pri_mem.block_memory_list)
            elif box_value == "Trabajo más corto":
                self.pri_mem.block_memory_list = second_order(self.pri_mem.block_memory_list)
            elif box_value == "FIFO":
                self.pri_mem.block_memory_list = third_order(self.pri_mem.block_memory_list)
            elif box_value == "Prioridad":
                self.pri_mem.block_memory_list = third_order(self.pri_mem.block_memory_list)
            self.add_process_table(self.table_memory_principal, self.pri_mem.block_memory_list)
            self.add_process_table(self.table_memory_secondary, self.sec_mem.block_memory_list)
    
    def print_tables(self):
        self.add_process_table(self.table_memory_principal, self.pri_mem.block_memory_list)
        blocks_with_data = [block for block in self.sec_mem.block_memory_list if block.data is not None]
        blocks_without_data = [block for block in self.sec_mem.block_memory_list if block.data is None]
        self.sec_mem.block_memory_list = blocks_with_data + blocks_without_data
        self.add_process_table(self.table_memory_secondary, self.sec_mem.block_memory_list)
    
    def calculate_global_prim_mem_used(self):
        memory_used = 0
        for block in self.pri_mem.block_memory_list:
            if block.data is not None:
                memory_used += block.data.size
        self.label_used__pri_mem.setText(str(memory_used)+" bytes")
        self.global_state.pri_memory_used = memory_used
    
    def calculate_global_sec_mem_used(self):
        memory_used = 0
        for block in self.sec_mem.block_memory_list:
            if block.data is not None:
                memory_used += block.data.size
        self.label_used__sec_mem.setText(str(memory_used)+" bytes")
        self.global_state.sec_memory_used = memory_used