import threading
import time
from util.states import ProcessState

class Process:
    def __init__(self, pid, state, name, priority, to_finish_time, executed_time, waiting_time, mem_limit):
        self.pid = pid
        self.state = ProcessState(state)
        self.name = name
        self.priority = priority
        self.to_finish_time = to_finish_time
        self.executed_time = executed_time
        self.waiting_time = waiting_time
        self.mem_limit = mem_limit
        self.thread = None

    def __str__(self):
        return f"Process {self.pid}: {self.name}"

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        while self.state != 'stopped':
            if self.state == 'running':
                # Simulate process execution
                time.sleep(1)
                self.executed_time += 1
                if self.executed_time >= self.to_finish_time:
                    self.state = 'stopped'
            elif self.state == 'paused':
                # Simulate process waiting
                time.sleep(1)
                self.waiting_time += 1

    def pause(self):
        if self.state == 'running':
            self.state = 'paused'

    def resume(self):
        if self.state == 'paused':
            self.state = 'running'

    def stop(self):
        self.state = 'stopped'