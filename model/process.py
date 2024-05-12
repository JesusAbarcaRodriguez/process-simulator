import threading
import time
from util.states import ProcessState

class Process:
    def __init__(self, pid, state,size, name, priority, to_finish_time, executed_time, waiting_time, mem_limit):
        self.pid = pid
        self.state = ProcessState(state)
        self.size = size
        self.name = name
        self.priority = priority
        self.to_finish_time = to_finish_time
        self.executed_time = executed_time
        self.waiting_time = waiting_time
        self.mem_limit = mem_limit
        self.thread = ProcessState.NEW
        self.lock = threading.Lock()

    def __str__(self):
        return f"Process {self.pid}: {self.name}"

    #   Admit the process
    #   Changes the state from new to ready
    def admit(self):
        with self.lock:
            if self.state == ProcessState.NEW:
                self.ready()
                self.run()

    #   Starts a thread to execute the process
    def run(self):
        with self.lock:
            if self.state == ProcessState.READY:
                self.state = ProcessState.RUNNING
                thread = threading.Thread(target=self.execute)
                thread.start()

    #   todo: timeout -> (running) -> (ready)
    #   Execute the process
    #   When the process is ready, it will start executing
    def execute(self, event=None):
        while self.executed_time < self.to_finish_time:
            with self.lock:
                if event and event.is_set():
                    self.block(event)
                else:
                    self.executed_time += 1
                    self.waiting_time += 1
                    time.sleep(1)
            if self.executed_time == self.to_finish_time:
                self.terminate()

    #   todo: suspend -> (blocked) -> (suspended_blocked)
    #   Block the process
    #   Changes the state from running to blocked
    def block(self, event=None):
        with self.lock:
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
        with self.lock:
            if self.state in [ProcessState.NEW, ProcessState.SUSPENDED_READY, ProcessState.BLOCKED]:
                self.state = ProcessState.READY 

    #   Activate the process
    #   Changes the state from suspended to ready/block
    #   - If the process is suspended_blocked, it will change to blocked
    #   - If the process is suspended_ready, it will change to ready
    def activate(self):
        with self.lock:
            if self.state == ProcessState.SUSPENDED_BLOCKED:
                self.state = ProcessState.BLOCKED
            elif self.state == ProcessState.SUSPENDED_READY:
                self.ready()

    #   Suspend the process
    #   Changes the state from blocked to suspended_blocked
    def suspended_block(self, event):
        with self.lock:
            if self.state == ProcessState.SUSPENDED_BLOCKED and not event.is_set():
                event.wait()
                self.state = ProcessState.SUSPENDED_READY

    #   Suspend the process
    #   Changes the state from ready to suspended_ready
    def suspended_ready(self):
        with self.lock:
            if self.state == ProcessState.READY:
                self.state = ProcessState.SUSPENDED_READY


    #   Terminate the process
    #   Changes the state from running to terminated
    def terminate(self):
        with self.lock:
            if self.state == ProcessState.RUNNING:
                self.state = ProcessState.TERMINATED
                self.thread.join()