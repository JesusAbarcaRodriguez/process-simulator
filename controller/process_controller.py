from model.process import Process
from util.states import ProcessState
import random

def create_processes(self, num_processes):
    self.process_list_primary_memory = []
    for i in range(1, num_processes + 1):
        sizes = [2**i for i in range(4, 10)]  # Genera las potencias de 2: 2, 4, 8, ..., 512
        proc_size = random.choice(sizes)
        to_finish_time_rand = proc_size / 5
        process = Process(i, ProcessState.RUNNING, proc_size, f"Process {i}", i%2+1, 0, 0, to_finish_time_rand)
        process.is_running = False
        self.process_list_primary_memory.append(process)
    self.num_process = len(self.process_list_primary_memory)
    return self.process_list_primary_memory

def suspend_process(self):
    if not self.id_process:
        return
    for block in self.pri_mem.block_memory_list:
        if block.is_process:
            if block.data and block.data.pid == self.id_process:
                block.data.suspended_block()
                self.sec_mem.block_memory_list = self.sec_mem.assign_proc_to_sec_mem(block.data)
                block.data = None
                break

    self.add_process_table(self.table_memory_principal, self.pri_mem.block_memory_list)
    self.add_process_table(self.table_memory_secondary, self.sec_mem.block_memory_list)

def assign_suspended_proc_to_pri_mem(self):
        if not self.id_process:
            return
        for block in self.sec_mem.block_memory_list:
            if block.data and block.data.pid == self.id_process:
                block.data.activate()
                self.pri_mem.block_memory_list = self.pri_mem.assign_proc_to_pri_mem(block.data)
                block.data = None
                break

def end_process(self):
    if self.id_process is not None:
        for block in self.pri_mem.block_memory_list:
            if block.data is not None:
                if block.data.pid == self.id_process:
                    block.data.terminate()
                    block.data = None
                    break
        self.add_process_table(self.table_memory_principal,self.pri_mem.block_memory_list)
    pass

def create_process(self,is_proc):
    self.num_process += 1
    priority_rand = random.randint(1, 10)
    sizes = [2**i for i in range(4, 10)]  # Genera las potencias de 2: 2, 4, 8, ..., 512
    proc_size = random.choice(sizes)
    to_finish_time_rand = proc_size / 5
    if is_proc:
        name = f"Process {self.num_process}"
        self.proc = Process(self.num_process, ProcessState.RUNNING, proc_size, name, priority_rand, 0, 0, to_finish_time_rand)
    else:
        name = f"Services {self.num_process}"
        self.proc = Process(self.num_process, ProcessState.RUNNING, proc_size, name, priority_rand, 0, 0, float('inf'))
    self.proc.is_running = False
    return self.proc