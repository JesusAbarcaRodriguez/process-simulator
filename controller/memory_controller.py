from model.memory import Memory
from model.block_memory import BlockMemory
from controller.process_controller import create_processes
from util.global_state import GlobalState
#   Initialize primary memory
def initialize_primary_memory(self,memory_size,num_processes):
    self.memory_principal = Memory(memory_size, 0, "Primary")
    self.memory_principal.block_memory_list = create_memory_blocks(self, memory_size,True)
    create_processes(self, num_processes)
    self.memory_principal.assign_memory(
        self.process_list_primary_memory)
    self.started = True
    return self.memory_principal

#   Initialize secondary memory
def initialize_secondary_memory(self,memory_size):
    self.memory_secondary = Memory(memory_size, 0, "Secondary")
    self.memory_secondary.block_memory_list = create_memory_blocks(self, memory_size,False)
    return self.memory_secondary

#   Create memory blocks
def create_memory_blocks(self, num_blocks,is_primary_memory):
    global_state = GlobalState()
    self.block_list = []
    sum_memory = 0
    for i in range(1, num_blocks + 1):
        block_size = 64*i
        block = BlockMemory(i, block_size, None)
        sum_memory += block_size
        self.block_list.append(block)
    if is_primary_memory:
        global_state.set_block_prim_memory_size(sum_memory)
    else:
        global_state.set_block_sec_memory_size(sum_memory)
    return self.block_list

def assign_page_to_pri_mem(self):
    for block in self.pri_mem.block_memory_list:
        for block_sec_mem in self.sec_mem.block_memory_list:
            if block_sec_mem.data is not None and block_sec_mem.is_process is False:
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