from model.process_table import ProcessTable
from util.states import ProcessState

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

    def assign_memory(self,process,block_memory_list):
        sorted(block_memory_list,key=lambda x: x.size)
        for i in range(0,len(block_memory_list) -1 ):
            for z in range(0,len(process) -1):
                if block_memory_list[i].proc is None and block_memory_list[i].size >= process[z].size and process[z].state == ProcessState.READY:
                    block_memory_list[i].proc = process[z]
                    process[z].state = ProcessState.ASSIGN
        return process,block_memory_list

    def assign_memory_secondary(self,process,block_memory_list):
        sorted(block_memory_list,key=lambda x: x.size)
        for i in range(0,len(block_memory_list) -1 ):
            for z in range(0,len(process) -1):
                if block_memory_list[i].proc is None and block_memory_list[i].size >= process[z].size and process[z].state == ProcessState.READY:
                    block_memory_list[i].proc = process[z]
        return process,block_memory_list