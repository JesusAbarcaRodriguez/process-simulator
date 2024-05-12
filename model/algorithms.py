def highest_response_rate(process):
    return process.waiting_time + process.to_finish_time / process.to_finish_time
def shortest_job_first(process):
    return process.to_finish_time + process.waiting_time
def priority(process):
    process.priority
def round_robin():
    pass
