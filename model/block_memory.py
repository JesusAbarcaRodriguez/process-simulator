class BlockMemory:
    is_process = True
    def __init__(self, block_id, size, proc):
        self.size = size
        self.block_id = block_id
        self.proc = proc