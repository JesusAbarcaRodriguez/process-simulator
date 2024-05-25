from model.algorithms import highest_response_rate, shortest_job_first
from util.states import ProcessState
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
    # Filtrar los bloques que tienen procesos y no son páginas
    processes_with_proc = [block for block in process if block.is_process and block.data is not None]

    # Ordenar los bloques por prioridad del proceso en orden descendente
    sorted_processes = sorted(processes_with_proc, key=lambda block: block.data.priority, reverse=True)

    # Actualizar el estado de los procesos según su nueva posición
    for i, block in enumerate(sorted_processes):
        if i == 0:
            block.data.admit()  # Poner en running el primer proceso de la lista ordenada
        else:
            if block.data.state == ProcessState.RUNNING:
                block.data.state = ProcessState.READY  # Cambiar a READY si estaba en RUNNING
            # Mantener el estado BLOQUEADO si ya estaba en ese estado
            # También puedes cambiar a un estado específico si es necesario

    # Mantener los bloques sin procesos en su lugar original
    processes_without_proc = [block for block in process if not block.is_process or block.data is None]

    # Combinar las listas manteniendo el orden original de los bloques sin procesos
    sorted_process = sorted_processes + processes_without_proc

    return sorted_process

