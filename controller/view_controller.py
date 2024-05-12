import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from model.block_memory import BlockMemory
from model.memory import Memory
from model.process import Process
from model.process_table import ProcessTable
from util.states import ProcessState
from PyQt5 import QtWidgets
from model.orders import third_order


class MainView(QMainWindow):

    process1 = Process(1, ProcessState.NEW,200, "Process 1", 1, 0, 0, 0, 0)
    process2 = Process(2, ProcessState.NEW, 100,"Process 2", 2, 5, 0, 0,0)
    process3 = Process(3, ProcessState.NEW, 20,"Process 3", 2, 15, 0, 0, 0)
    process4 = Process(4, ProcessState.NEW, 40,"Process 4", 1, 7, 0, 0, 0)

    process_list = [process1, process2, process3, process4]

    block1_secondary = BlockMemory(1, 100,None)
    block2_secondary = BlockMemory(2, 200, None)
    block3_secondary = BlockMemory(3, 300, None)
    block4_secondary = BlockMemory(4, 400, None)
    block5_secondary = BlockMemory(5, 500, None)
    block6_secondary = BlockMemory(6, 600, None)
    block7_secondary = BlockMemory(7, 700, None)
    block8_secondary = BlockMemory(8, 800, None)
    block9_secondary = BlockMemory(9, 900, None)
    block10_secondary = BlockMemory(10, 1000, None)

    block_secondary_list = [block1_secondary, block2_secondary, block3_secondary, block4_secondary, block5_secondary, block6_secondary, block7_secondary, block8_secondary, block9_secondary, block10_secondary]

    memory = Memory(10000, 0,"Secondary")

    process,block_secondary_list=memory.assign_memory_secondary(process_list, block_secondary_list)

    block1 = BlockMemory(1, 100,None)
    block2 = BlockMemory(2, 200, None)
    block3 = BlockMemory(3, 300, None)
    block4 = BlockMemory(4, 400, None)

    block_memory_list = [block1, block2, block3, block4]

    memory = Memory(10000, 0,"Primary")

    process_list,block_memory_list =  memory.assign_memory(process_list, block_memory_list)

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
        self.table_process.setColumnWidth(4, 197)
        self.table_process.setColumnWidth(5, 197)
        self.table_process.setColumnWidth(6, 120)
        # Verificar si el layout está configurado correctamente
        self.add_process_table(self.process_list)
        if self.frame_inferior1.layout() is None:
            self.frame_inferior1.setLayout(QtWidgets.QVBoxLayout()) # Configurar un QVBoxLayout
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