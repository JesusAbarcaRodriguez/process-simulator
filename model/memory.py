from model.process_table import ProcessTable

class Memory:
    def __init__(self, max_size):
        self.max_size = max_size
        self.current_size = 0
        self.process_table = ProcessTable()

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