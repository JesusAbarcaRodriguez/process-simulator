
#   todo: logic with different types of memory
#   principal memory
#   secondary memory
#   virtual memory
class Memory:
    block_memory_list=[]

    def __init__(self, max_size, current_size, type_memory):
        self.max_size = max_size
        self.current_size = current_size
        self.type_memory = type_memory

    #   assign memory blocks to processes
    def assign_memory(self, block_secondary_list, memory_secondary):
        is_assigned = False
        for block_secondary in block_secondary_list:
            if block_secondary.proc is not None:
                for block_primary in self.block_memory_list:
                    if block_primary.proc is None and block_primary.size >= block_secondary.proc.size and self.current_size < self.max_size:
                        block_primary.proc = block_secondary.proc
                        block_secondary.proc = None
                        is_assigned = True
                        memory_secondary.current_size -= 1
                        self.current_size += 1
                        break
        return block_secondary_list, self.block_memory_list, is_assigned, self, memory_secondary      

    # todo: new, suspended_ready, suspended_blocked
    def assign_memory_secondary(self, process):
        for process_item in process:
            for block in self.block_memory_list:
                if block.proc is None and block.size >= process_item.size and self.current_size < self.max_size:
                    block.proc = process_item
                    self.current_size += 1
                    break
        return self.block_memory_list

    # place type of memory in param
    def assign_proc_to_sec_mem(self, process):
        for block in self.block_memory_list:
            if block.proc is None and block.size >= process.size:
                block.proc = process
                break
        return self.block_memory_list