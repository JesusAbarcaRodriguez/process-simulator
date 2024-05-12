from model.algorithms import highest_response_rate, shortest_job_first
def first_order(process):
    for i in range(0,len(process)):
        if highest_response_rate(process[i]) < highest_response_rate(process[i+1]):
            process[i], process[i+1] = process[i+1], process[i]
    return process
def second_order(process):
    for i in range(0,len(process)):
        if shortest_job_first(process[i]) > shortest_job_first(process[i+1]):
            process[i], process[i+1] = process[i+1], process[i]
    return process
def third_order(process):
    for i in range(0,len(process)):
        if process[i].priority < process[i+1].priority:
            process[i], process[i+1] = process[i+1], process[i]
    return process