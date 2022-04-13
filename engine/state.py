"""
State Handling file for engine

- State object
- State handling methods
- state queue

"""

from engine import handler, world
from collections import deque


STATEQUEUE = deque()
CURRENT = None


class State(handler.Handler, world.World):
    def __init__(self):
        """
        State constructor for states
        
        Extends off both the Handler and World objects
        - allows for entity handling
        - and chunk handling
        
        """
        handler.Handler.__init__(self)
        world.World.__init__(self)
    
    def start(self) -> None:
        """to be overriden by child class - should load the level or whatever it needs to load"""
        pass

    def update(self, dt: float, rel_center: tuple = (0, 0)) -> None:
        """update the state and its handler"""
        self.render_chunks(rel_center)
        self.handle_entities(dt)


def push_state(state: State) -> None:
    """push a new state onto the state stack"""
    global CURRENT
    state.start()
    CURRENT = state
    STATEQUEUE.append(state)


def previous_state(state: State) -> None:
    """go back go back!"""
    STATEQUEUE.pop()
    global CURRENT
    CURRENT = None
    if STATEQUEUE:
        CURRENT = STATEQUEUE[-1]



