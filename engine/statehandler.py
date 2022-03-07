
from collections import deque


QUEUE = deque()
CURRENT = None

def push_state(state):
    """push a new state onto the stack"""
    global CURRENT
    QUEUE.append(state)
    CURRENT = state


