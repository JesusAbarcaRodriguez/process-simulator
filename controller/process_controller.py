from model.process import Process
from util.states import ProcessState

#   Create a number of processes, and return a list of them
def create_processes(self, num_processes):
    self.process_list_secondary_memory = []
    for i in range(1, num_processes + 1):
        process = Process(i, ProcessState.NEW, i*50, f"Process {i}", i%2+1, i*5, 0, 0, 0)
        self.process_list_secondary_memory.append(process)
    self.num_process = len(self.process_list_secondary_memory)
    return self.process_list_secondary_memory