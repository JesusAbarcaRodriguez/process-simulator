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
        self._initialized = True

    def set_pri_mem_size(self, size):
        self.pri_mem_size = size

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

