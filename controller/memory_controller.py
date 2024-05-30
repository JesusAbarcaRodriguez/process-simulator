from model.memory import Memory
from model.block_memory import BlockMemory
from controller.process_controller import create_processes

#   Initialize primary memory
def initialize_primary_memory(self,memory_size,num_processes):
    self.memory_principal = Memory(memory_size, 0, "Primary")
    self.memory_principal.block_memory_list = create_memory_blocks(self, memory_size)
    create_processes(self, num_processes)
    self.memory_principal.assign_memory(
        self.process_list_primary_memory)
    self.started = True
    return self.memory_principal

#   Initialize secondary memory
def initialize_secondary_memory(self,memory_size):
    self.memory_secondary = Memory(memory_size, 0, "Secondary")
    self.memory_secondary.block_memory_list = create_memory_blocks(self, memory_size)
    return self.memory_secondary

#   Create memory blocks
def create_memory_blocks(self, num_blocks):
    self.block_list = []
    for i in range(1, num_blocks + 1):
        block = BlockMemory(i, i*100, None)
        self.block_list.append(block)
    return self.block_list

def assign_page_to_pri_mem(self):
    for block in self.pri_mem.block_memory_list:
        for block_sec_mem in self.sec_mem.block_memory_list:
            if block_sec_mem.data is not None:
                if block.data is None and block.size >= block_sec_mem.data.size:
                    if block_sec_mem.is_process:
                        block.is_process = True
                    else:
                        block.is_process = False
                    block.data = block_sec_mem.data
                    self.pri_mem.current_size += 1
                    self.sec_mem.current_size -= 1
                    block.is_process = False
                    block_sec_mem.data = None
                    break
    return self.pri_mem.block_memory_list, self.sec_mem.block_memory_list