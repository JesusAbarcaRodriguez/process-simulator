from model.memory import Memory
from model.block_memory import BlockMemory
from controller.process_controller import create_processes

#   Initialize primary memory
def initialize_primary_memory(self):
    self.memory_principal = Memory(10, 0, "Primary")
    self.memory_principal.block_memory_list = create_memory_blocks(self, 10)
    create_processes(self, 4)
    self.memory_principal.assign_memory(
        self.process_list_primary_memory)
    self.started = True
    return self.memory_principal

#   Initialize secondary memory
def initialize_secondary_memory(self):
    self.memory_secondary = Memory(20, 0, "Secondary")
    self.memory_secondary.block_memory_list = create_memory_blocks(self, 20)
    return self.memory_secondary

#   Create memory blocks
def create_memory_blocks(self, num_blocks):
    self.block_list = []
    for i in range(1, num_blocks + 1):
        block = BlockMemory(i, i*100, None)
        self.block_list.append(block)
    return self.block_list