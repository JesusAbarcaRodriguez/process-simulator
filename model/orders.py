from model.algorithms import highest_response_rate, shortest_job_first
# Change to block_list instead of process_list
def first_order(process):
    for i in range(0,len(process) -1):
        if highest_response_rate(process[i].proc) < highest_response_rate(process[i+1].proc):
            process[i].proc, process[i+1].proc = process[i+1].proc, process[i].proc
    return process

def second_order(process):
    for i in range(0,len(process) -1 ):
        if shortest_job_first(process[i].proc) > shortest_job_first(process[i+1].proc):
            process[i].proc, process[i+1].proc = process[i+1].proc, process[i].proc
    return process

def third_order(process):
    # Filtrar los bloques que tienen procesos
    processes_with_proc = [block for block in process if block.proc is not None]

    # Ordenar los bloques por prioridad del proceso en orden descendente
    sorted_processes = sorted(processes_with_proc, key=lambda block: block.proc.priority, reverse=True)

    # Mantener los bloques sin procesos en su lugar original
    processes_without_proc = [block for block in process if block.proc is None]

    # Combinar las listas
    sorted_process = sorted_processes + processes_without_proc

    return sorted_process
