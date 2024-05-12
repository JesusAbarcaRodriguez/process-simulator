from enum import Enum

class ProcessState(Enum):
    NEW = 'new'
    READY = 'ready'
    RUNNING = 'running'
    BLOCKED = 'blocked'
    SUSPENDED_READY = 'suspended_ready'
    SUSPENDED_BLOCKED = 'suspended_blocked'
    TERMINATED = 'terminated'
