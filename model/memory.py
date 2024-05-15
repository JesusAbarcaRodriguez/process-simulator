from model.process_table import ProcessTable
from util.states import ProcessState
from model.process import Process

#   todo: logic with different types of memory
#   principal memory
#   secondary memory
#   virtual memory
class Memory:
    block_memory_list=[]
    def __init__(self, max_size, current_size,type_memory):
        self.max_size = max_size
        self.current_size = current_size
        self.type_memory = type_memory

    def add_process(self, process):
        if self.current_size < self.max_size:
            self.process_table.add_process(process)
            self.current_size += process.mem_limit

    def remove_process(self, pid):
        process = self.process_table.find_process(pid)
        if process:
            self.process_table.remove_process(pid)
            self.current_size -= process.mem_limit

    def get_process(self, pid):
        return self.process_table.find_process(pid)

    #   todo: should come from secondary memory as (new)
    #   from secondary_memory_list to primary_memory_list
    #   delete process from secondary_memory_list
    #   Assign memory to processes
    #   order memory blocks by size
    #   assign memory blocks to processes
    def assign_memory(self,block_secondary_list,block_primary_list,memory_principal,memory_secondary):
        is_assigned = False
        for block_secondary in block_secondary_list:
            if block_secondary.proc is not None:
                for block_primary in block_primary_list:
                    if block_primary.proc is None and block_primary.size >= block_secondary.proc.size and memory_principal.current_size < memory_principal.max_size:
                        block_primary.proc = block_secondary.proc
                        block_secondary.proc = None
                        is_assigned = True
                        memory_secondary.current_size -= 1
                        memory_principal.current_size += 1
                        break
        return block_secondary_list, block_primary_list, is_assigned, memory_principal, memory_secondary      

    # todo: new, suspended_ready, suspended_blocked
    def assign_memory_secondary(self, process, block_memory_list,memory_secondary):
        for process_item in process:
            for block in block_memory_list:
                if block.proc is None and block.size >= process_item.size and memory_secondary.current_size < memory_secondary.max_size:
                    block.proc = process_item
                    memory_secondary.current_size += 1
                    break
        return block_memory_list

    def assign_proc_to_memory_secondary(self,proc,block_memory_list):
        for block in block_memory_list:
            if block.proc is None and block.size >= proc.size:
                block.proc = proc
                break
        return block_memory_list

    def update_block_memory_list(self, process, memory_secondary):
        self.block_memory_list = self.assign_memory_secondary(process, self.block_memory_list, memory_secondary)
