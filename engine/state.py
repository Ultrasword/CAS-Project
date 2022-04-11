"""
State Handling file for engine

- State object
- State handling methods
- state queue

"""


from collections import deque


STATEQUEUE = deque()
CURRENT = None


def push_state(state):
    """push a new state onto the state stack"""
    global CURRENT
    CURRENT = state
    STATEQUEUE.append(state)


def previous_state(state):
    """go back go back!"""
    STATEQUEUE.pop()
    global CURRENT
    CURRENT = None
    if STATEQUEUE:
        CURRENT = STATEQUEUE[-1]



class State:
    def __init__(self):
        """State constructor for states"""
        self.handler = None
    
    def set_handler(self, handler):
        """sets the handler for this state"""
        self.handler = handler

    def update_state(self, window, dt):
        """update the state and its handler"""
        # assume there is a handler object
        self.handler.handle_entities(window, dt)




