import random
import threading
import time
from model.page import Page
from util.states import ProcessState

class Process:
    is_running = False
    list_position = 0
    # remove state by param
    def __init__(self, pid, state,size, name, priority,  executed_time, waiting_time, to_finish_time):
        self.pid = pid
        self.state = ProcessState(state)
        self.size = size
        self.name = name
        self.priority = priority
        self.to_finish_time = to_finish_time
        self.executed_time = executed_time
        self.waiting_time = waiting_time
        
        # self.lock = threading.Lock()

    def __str__(self):
        return f"Process {self.pid}: {self.name}"

    #   Admit the process
    #   Changes the state from new to ready
    def admit(self):
        if self.state == ProcessState.RUNNING:
            self.run()

    #   Starts a thread to execute the process
    def run(self):
        thread = threading.Thread(target=self.execute)
        thread.start()

    #   todo: timeout -> (running) -> (ready)
    #   calculate to_finish_time
    #   calculate memory size (principal, virtual)
    #   Execute the process
    #   When the process is ready, it will start executing
    def execute(self, event=None):
        time.sleep(2 * self.list_position)
        self.executed_time +=1

    #   Suspend the process
    #   Changes the state from ready to suspended_ready
    def suspended_block(self):
        if self.state == ProcessState.RUNNING:
            self.state = ProcessState.SUSPENDED_BLOCKED

    #   Terminate the process
    #   Changes the state from running to terminated
    def terminate(self):
        if self.state == ProcessState.RUNNING:
            self.state = ProcessState.TERMINATED
    
    def divide_into_pages(self, page_size):
        pages = []
        num_pages = (self.size + page_size - 1) // page_size  # Calcula el número de páginas necesarias
        time_per_page = self.to_finish_time / num_pages
        for i in range(num_pages):
            page_id = f"{self.pid}-{i}"
            pages.append(Page(page_id, min(page_size, self.size - i * page_size), self, i, self.priority, time_per_page, 0, 0,ProcessState.RUNNING))
        return pages