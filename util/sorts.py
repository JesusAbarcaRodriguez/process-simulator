from util.algorithms import highest_response_rate, shortest_job_first

def first_order(block_memory_list):
    blocks_with_data = [block for block in block_memory_list if block.data is not None]
    blocks_without_data = [block for block in block_memory_list if block.data is None]
    
    sorted_items = sorted(blocks_with_data, key=lambda block: highest_response_rate(block.data), reverse=True)
    for i in range(0, len(sorted_items)):
        sorted_items[i].data.list_position = i
    sorted_block_memory_list = sorted_items + blocks_without_data
    return sorted_block_memory_list

def second_order(block_memory_list):
    blocks_with_data = [block for block in block_memory_list if block.data is not None]
    blocks_without_data = [block for block in block_memory_list if block.data is None]
    
    sorted_items = sorted(blocks_with_data, key=lambda block: shortest_job_first(block.data))
    for i in range(0, len(sorted_items)):
        sorted_items[i].data.list_position = i

    sorted_block_memory_list = sorted_items + blocks_without_data
    return sorted_block_memory_list

def third_order(block_memory_list):
    blocks_with_data = [block for block in block_memory_list if block.data is not None]
    blocks_without_data = [block for block in block_memory_list if block.data is None]
    
    sorted_items = sorted(blocks_with_data, key=lambda block: block.data.priority, reverse=True)
    for i in range(0, len(sorted_items)):
        sorted_items[i].data.list_position = i

    sorted_block_memory_list = sorted_items + blocks_without_data
    return sorted_block_memory_list
