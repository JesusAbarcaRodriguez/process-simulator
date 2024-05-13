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
    def assign_memory(self, process: Process, block_memory_list):
        sorted(block_memory_list,key=lambda x: x.size)
        allocated_processes = []
        for i in range(0,len(block_memory_list) -1 ):
            for z in range(0,len(process) -1):
                if block_memory_list[i].proc is None and block_memory_list[i].size >= process[z].size:
                    block_memory_list[i].proc = process[z]
                    allocated_processes.append(process[z])
                    break
        primary_process = process
        for i in range(0,len(allocated_processes) -1):
            for z in range(0,len(process) -1):
                if allocated_processes[i].pid == process[z].pid:
                    process.remove(allocated_processes[i])
        return primary_process, block_memory_list,process

    # todo: new, suspended_ready, suspended_blocked
    def assign_memory_secondary(self,process,block_memory_list):
        sorted(block_memory_list,key=lambda x: x.size)
        for i in range(0,len(block_memory_list) -1 ):
            for z in range(0,len(process) -1):
                if block_memory_list[i].proc is None and block_memory_list[i].size >= process[z].size:
                    block_memory_list[i].proc = process[z]
        return process,block_memory_list