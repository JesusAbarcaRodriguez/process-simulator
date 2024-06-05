
#   todo: logic with different types of memory
#   principal memory
#   secondary memory
#   virtual memory
from util.message import show_error_message
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
                if block.data is None and block.size >= process_item.size and self.current_size < self.max_size:
                    block.data = process_item
                    self.current_size += 1
                    block.is_process = True
                    break
        return self.block_memory_list

    def is_memory_full_to_process(self):
        if self.current_size >= self.max_size-2:
            return True
        return False
    def is_memory_full_to_pages(self):
        if self.current_size >= self.max_size:
            return True
        return False
    # place type of memory in param
    def assign_proc_to_pri_mem(self,data):
        is_assigned = False
        for block in self.block_memory_list:
            if block.data is None and block.size >= data.size:
                block.data = data
                self.current_size += 1
                block.is_process = True
                is_assigned = True
                break
        return self.block_memory_list,is_assigned
    
    def assign_proc_to_sec_mem(self, process):
        for block in self.block_memory_list:
            if block.data is None and block.size >= process.size:
                block.data = process
                self.current_size += 1
                block.is_process = True
                break
        return self.block_memory_list
    
    def assign_page_to_pri_mem(self, page):
        for block in self.block_memory_list:
            if block.data is None and block.size >= page.size:
                block.data = page
                self.current_size += 1
                block.is_process = False
                break
        return self.block_memory_list

    def assign_page_to_sec_mem(self, page):
        for block in self.block_memory_list:
            if block.data is None and block.size >= page.size:
                block.data = page
                self.current_size += 1
                block.is_process = False
                break
        return self.block_memory_list