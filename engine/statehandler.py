
from collections import deque


QUEUE = deque()
CURRENT = None

def push_state(state):
    global CURRENT
    QUEUE.append(state)
    CURRENT = state


