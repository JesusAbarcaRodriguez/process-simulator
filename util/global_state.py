def singleton(cls):
    instances = {}
    def wraps(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wraps

@singleton
class GlobalState(object):
    def __init__(self):
        self.pri_mem_size = 0
        self.sec_mem_size = 0
        self.initial_processes = 0
        self.block_sec_memory_size = 0
        self.pri_memory_used = 0
        self.sec_memory_used = 0
        self.block_prim_memory_size = 0
        self._initialized = True

    def set_pri_mem_size(self, size):
        self.pri_mem_size = size

    def set_block_sec_memory_size(self, size):
        self.block_memory_size = size
    
    def set_block_prim_memory_size(self, size):
        self.block_prim_memory_size = size

    def set_pri_memory_used(self, size):
        self.pri_memory_used = size
    
    def set_sec_memory_used(self, size):
        self.sec_memory_used = size
    
    def set_sec_mem_size(self, size):
        self.sec_mem_size = size

    def set_initial_processes(self, count):
        self.initial_processes = count

    def get_pri_mem_size(self):
        return self.pri_mem_size

    def get_sec_mem_size(self):
        return self.sec_mem_size

    def get_initial_processes(self):
        return self.initial_processes
    
    def get_block_sec_memory_size(self):
        return self.block_memory_size
    
    def get_block_prim_memory_size(self):
        return self.block_prim_memory_size
    
    def get_pri_memory_used(self):
        return self.pri_memory_used
    
    def get_sec_memory_used(self):
        return self.sec_memory_used