from model.algorithms import highest_response_rate, shortest_job_first
from util.states import ProcessState
# Change to block_list instead of process_list
def first_order(process):
    for i in range(0,len(process) -1):
        if highest_response_rate(process[i].data) < highest_response_rate(process[i+1].data):
            process[i].data, process[i+1].data = process[i+1].data, process[i].data
    return process

def second_order(process):
    for i in range(0,len(process) -1 ):
        if shortest_job_first(process[i].data) > shortest_job_first(process[i+1].data):
            process[i].data, process[i+1].data = process[i+1].data, process[i].data
    return process

def third_order(block_memory_list):
    blocks_with_data = [block for block in block_memory_list if block.data is not None]
    blocks_without_data = [block for block in block_memory_list if block.data is None]
    for i in range(0,len(blocks_with_data) -1):
        if blocks_with_data[i].data is not None and blocks_with_data[i+1].data is not None:
            priority1 = blocks_with_data[i].data.priority
            priority2 = blocks_with_data[i+1].data.priority
            if priority1 < priority2:
                blocks_with_data[i], blocks_with_data[i+1] = blocks_with_data[i+1], blocks_with_data[i]
    blocks_with_data[0].data.state = ProcessState.RUNNING
    for i in range(1,len(blocks_with_data) -1):
        if blocks_with_data[i].data is not None:
            if blocks_with_data[i].data.state == ProcessState.RUNNING:
                blocks_with_data[i].data.state = ProcessState.READY  # Cambiar a READY si estaba en RUNNING
    
    sorted_block_memory_list = blocks_with_data + blocks_without_data
    return sorted_block_memory_list