import random
import threading
import time
from model.page import Page
from util.states import ProcessState

class Process:
    pages = []
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
        self.thread = ProcessState.NEW
        
        # self.lock = threading.Lock()

    def __str__(self):
        return f"Process {self.pid}: {self.name}"

    #   Admit the process
    #   Changes the state from new to ready
    def admit(self):
        if self.state == ProcessState.READY:
            self.run()

    #   Starts a thread to execute the process
    def run(self):
        if self.state == ProcessState.READY:
            self.state = ProcessState.RUNNING
            thread = threading.Thread(target=self.execute)
            thread.start()

    #   todo: timeout -> (running) -> (ready)
    #   calculate to_finish_time
    #   calculate memory size (principal, virtual)
    #   Execute the process
    #   When the process is ready, it will start executing
    def execute(self, event=None):
        while self.executed_time < self.to_finish_time and self.state == ProcessState.RUNNING:
                # if event and event.is_set():
                    # self.block(event)
                # else:
            self.executed_time += round(random.uniform(1, 3), 2)
            time.sleep(1)
            if self.executed_time == self.to_finish_time:
                time.sleep(1)
                self.terminate()

    #   todo: suspend -> (blocked) -> (suspended_blocked)
    #   Block the process
    #   Changes the state from running to blocked
    def block(self, event=None):
        if self.state == ProcessState.RUNNING:
            self.state = ProcessState.BLOCKED
            if event:
                event.clear()
                event.wait()
                self.ready()

    #   todo: suspend -> (ready) -> (suspended_ready)
    #   Prepare the process
    #   Changes the state from new, blocked, suspended_ready to ready 
    def ready(self):
        if self.state in [ProcessState.NEW, ProcessState.SUSPENDED_READY, ProcessState.BLOCKED]:
            self.state = ProcessState.READY 

    #   Activate the process
    #   Changes the state from suspended to ready/block
    #   - If the process is suspended_blocked, it will change to blocked
    #   - If the process is suspended_ready, it will change to ready
    def activate(self):
        if self.state == ProcessState.SUSPENDED_BLOCKED:
            self.state = ProcessState.BLOCKED
        elif self.state == ProcessState.SUSPENDED_READY:
            self.ready()

    #   Suspend the process
    #   Changes the state from blocked to suspended_blocked
    def suspended_block(self):
        if self.state == ProcessState.BLOCKED or self.state == ProcessState.RUNNING:
            self.state = ProcessState.SUSPENDED_BLOCKED

    #   Suspend the process
    #   Changes the state from ready to suspended_ready
    def suspended_ready(self):
        if self.state == ProcessState.READY:
            self.state = ProcessState.SUSPENDED_READY


    #   Terminate the process
    #   Changes the state from running to terminated
    def terminate(self):
        if self.state == ProcessState.RUNNING:
            self.state = ProcessState.TERMINATED
            self.thread.join()
    
    def divide_into_pages(self, page_size):
        num_pages = (self.size + page_size - 1) // page_size  # Calcula el número de páginas necesarias
        for i in range(num_pages):
            page_id = f"{self.pid}-{i}"
            self.pages.append(Page(page_id, min(page_size, self.size - i * page_size), self, i))
        return self.pages