import threading
import time
from model.page import Page
from util.states import ProcessState
import random
class Service:
    is_running = False
    list_position = 0
    def __init__(self, pid, state,size, name, priority,  executed_time, waiting_time, to_finish_time):
        self.pid = pid
        self.state = ProcessState(state)
        self.size = size
        self.name = name
        self.priority = priority
        self.to_finish_time = to_finish_time
        self.executed_time = executed_time
        self.waiting_time = waiting_time
        
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

    #   Suspend the process
    #   Changes the state from ready to suspended_ready
    def suspended_block(self):
        if self.state == ProcessState.RUNNING:
            self.state = ProcessState.SUSPENDED_BLOCKED

    #   todo: timeout -> (running) -> (ready)
    #   calculate to_finish_time
    #   calculate memory size (principal, virtual)
    #   Execute the process
    #   When the process is ready, it will start executing
    def execute(self, event=None):
        time.sleep(2 * self.list_position)
        self.executed_time +=1

    #   Terminate the process
    #   Changes the state from running to terminated
    def terminate(self):
        if self.state == ProcessState.RUNNING:
            self.state = ProcessState.TERMINATED

def create_service(self):
    self.num_process += 1
    name = f"Service {self.num_process}"
    priority_rand = random.randint(1, 10)
    self.service = Service(self.num_process, ProcessState.RUNNING, 100, name, priority_rand, 0, 0, float('inf'))
    self.service.is_running = False
    return self.service