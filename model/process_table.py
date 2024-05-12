class ProcessTable:
    def __init__(self,processes = []):
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def remove_process(self, pid):
        self.processes = [p for p in self.processes if p.pid != pid]

    def find_process(self, pid):
        for process in self.processes:
            if process.pid == pid:
                return process
        return None