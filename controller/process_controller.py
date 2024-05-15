from model.process import Process
from util.states import ProcessState
from model.block_memory import BlockMemory
from model.memory import Memory

# How it is refactored
def prepare_program(self):
    initialize_secondary_memory(self)
    initialize_primary_memory(self)

def initialize_primary_memory(self):
    self.memory_principal = Memory(20, 0, "Primary")
    self.memory_principal.block_memory_list = create_memory_blocks(self, 5)
    return self.memory_principal

def initialize_secondary_memory(self):
    self.memory_secondary = Memory(10, 0, "Secondary")
    self.memory_secondary.block_memory_list = create_memory_blocks(self, 10)
    create_processes(self, 4)
    self.memory_secondary.assign_memory_secondary(
        self.process_list_secondary_memory, 
        self.memory_secondary.block_memory_list, 
        self.memory_secondary)
    self.started = True
    return self.memory_secondary

def create_processes(self, num_processes):
    self.process_list_secondary_memory = []
    for i in range(1, num_processes + 1):
        process = Process(i, ProcessState.NEW, i*50, f"Process {i}", i%2+1, i*5, 0, 0, 0)
        self.process_list_secondary_memory.append(process)
    self.num_process = len(self.process_list_secondary_memory)
    return self.process_list_secondary_memory

def create_memory_blocks(self, num_blocks):
    self.block_secondary_list = []
    for i in range(1, num_blocks + 1):
        block = BlockMemory(i, i*100, None)
        self.block_secondary_list.append(block)
    return self.block_secondary_list