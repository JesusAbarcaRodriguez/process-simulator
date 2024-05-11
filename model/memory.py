class Memory:
    def __init__(self, max_size):
        self.max_size = max_size
        self.current_size = 0
        self.processes = []
    def add_process(self, process):
        self.processes.append(process)
        self.current_size += 1
    def remove_process(self, process):
        self.processes.remove(process)
        self.current_size -= 1
    def get_process(self, index):
        return self.processes[index]
    def highest_response_rate():
        pass
    def shortest_job_first():
        pass
    def priority():
        pass