class Page:
    def __init__(self, page_id, size, process, page_number, priority, to_finish_time, executed_time, waiting_time   ):
        self.page_id = page_id
        self.size = size
        self.process = process
        self.page_number = page_number
        self.priority = priority
        self.to_finish_time = to_finish_time
        self.executed_time = executed_time
        self.waiting_time = waiting_time

def create_pages(self):
    page_size = 10  # Tamaño de página arbitrario, ajústalo según tus necesidades
    self.proc.pages = self.proc.divide_into_pages(page_size)

    # Intentar agregar las páginas a la memoria principal y secundaria
    for page in self.proc.pages:
        if not self.pri_mem.is_memory_full_to_pages():
            self.pri_mem.block_memory_list = self.pri_mem.assign_page_to_pri_mem(page)
        else:
            self.sec_mem.block_memory_list = self.sec_mem.assign_page_to_sec_mem(page)

    return self.pri_mem.block_memory_list, self.sec_mem.block_memory_list

def assign_page_to_pri_mem(self):
    for block in self.sec_mem.block_memory_list:
        if block.is_process is False and self.pri_mem.is_memory_full_to_pages() == False:
            self.pri_mem.block_memory_list = self.pri_mem.assign_page_to_pri_mem(block.proc)
            block.proc = None
            self.sec_mem.current_size -= 1
    return self.pri_mem.block_memory_list, self.sec_mem.block_memory_list
