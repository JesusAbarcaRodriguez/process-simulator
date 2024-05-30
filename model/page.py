from util.message import show_error_message
from util.states import ProcessState
import threading
import time
class Page:
    list_position = 0
    is_running = False
    def __init__(self, page_id, size, process, page_number, priority, to_finish_time, executed_time, waiting_time,state   ):
        self.page_id = page_id
        self.size = size
        self.process = process
        self.page_number = page_number
        self.priority = priority
        self.to_finish_time = to_finish_time
        self.executed_time = executed_time
        self.waiting_time = waiting_time
        self.state = ProcessState(state)

    def admit(self):
        if self.state == ProcessState.RUNNING:
            self.run()

    #   Suspend the process
    #   Changes the state from ready to suspended_ready
    def suspended_block(self):
        if self.state == ProcessState.RUNNING:
            self.state = ProcessState.SUSPENDED_BLOCKED

    #   Starts a thread to execute the process
    def run(self):
        thread = threading.Thread(target=self.execute)
        thread.start()

    #   Terminate the process
    #   Changes the state from running to terminated
    def terminate(self):
        if self.state == ProcessState.RUNNING:
            self.state = ProcessState.TERMINATED
            
    #   todo: timeout -> (running) -> (ready)
    #   calculate to_finish_time
    #   calculate memory size (principal, virtual)
    #   Execute the process
    #   When the process is ready, it will start executing
    def execute(self, event=None):
        time.sleep(2 * self.list_position)
        self.executed_time +=1


def create_pages(self):
    page_size = 10  # Tamaño de página arbitrario, ajústalo según tus necesidades
    self.proc.pages = self.proc.divide_into_pages(page_size)

    if len(self.proc.pages) + self.sec_mem.current_size > self.sec_mem.max_size:
        show_error_message(self, "Error", "No hay suficiente memoria secundaria para asignar las páginas.")
        return self.pri_mem.block_memory_list, self.sec_mem.block_memory_list
    # Intentar agregar las páginas a la memoria principal y secundaria
    for page in self.proc.pages:
        if not self.pri_mem.is_memory_full_to_pages():
            self.pri_mem.block_memory_list = self.pri_mem.assign_page_to_pri_mem(page)
        else:
            self.sec_mem.block_memory_list = self.sec_mem.assign_page_to_sec_mem(page)

    return self.pri_mem.block_memory_list, self.sec_mem.block_memory_list

def assign_page_to_pri_mem(self):
    for block in self.sec_mem.block_memory_list:
        if block.is_process is False and self.pri_mem.is_memory_full_to_pages() == False:
            self.pri_mem.block_memory_list = self.pri_mem.assign_page_to_pri_mem(block.proc)
            block.proc = None
            self.sec_mem.current_size -= 1
    return self.pri_mem.block_memory_list, self.sec_mem.block_memory_list
