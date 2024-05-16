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
def suspend_process(self):
        if self.id_process is not None:
            for block in self.pri_mem.block_memory_list:
                if block.proc is not None:
                    if block.proc.pid == self.id_process:
                        block.proc.state = ProcessState.SUSPENDED_BLOCKED
                        self.sec_mem.block_memory_list = self.sec_mem.assign_proc_to_sec_mem(block.proc)
                        block.proc = None
                        break
            self.add_process_table_primary(self.pri_mem.block_memory_list)
            self.add_process_table_secondary(self.sec_mem.block_memory_list)