
#   todo: logic with different types of memory
#   principal memory
#   secondary memory
#   virtual memory
from util.states import ProcessState

class Memory:
    block_memory_list=[]

    def __init__(self, max_size, current_size, type_memory):
        self.max_size = max_size
        self.current_size = current_size
        self.type_memory = type_memory

    #   assign memory blocks to processes
    def assign_memory(self, process):
        for process_item in process:
            for block in self.block_memory_list:
                if block.proc is None and block.size >= process_item.size and self.current_size < self.max_size:
                    block.proc = process_item
                    self.current_size += 1
                    block.is_process = True
                    break
        return self.block_memory_list

    # place type of memory in param
    def assign_proc_to_pri_mem(self, process):
        for block in self.block_memory_list:
            if block.proc is None and block.size >= process.size:
                block.proc = process
                self.current_size += 1
                block.is_process = True
                break
        return self.block_memory_list
    
    def assign_page_to_pri_mem(self, page):
        for block in self.block_memory_list:
            if block.proc is None and block.size >= page.size:
                block.proc = page
                self.current_size += 1
                block.is_process = False
                break
        return self.block_memory_list

    def assign_page_to_sec_mem(self, page):
        for block in self.block_memory_list:
            if block.proc is None and block.size >= page.size:
                block.proc = page
                self.current_size += 1
                block.is_process = False
                break
        return self.block_memory_list