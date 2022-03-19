from collections import deque


"""
Event handler system

- you have the event registered into a dict
- each event will have an id - integer
- when an event is announced, every registered entity will recieve the command and run respective functions
- ggs

"""

events = deque()

def add_event(event_data_block):
    """Append events to the events deque"""
    events.append(event_data_block)


def update_events():
    """Update all events with registered objects"""
    for event in events:
        call_event(event.eid, event.data)
    events.clear()


REGISTERED_EVENTS = {} # a eid and event pair
REGISTERED_OBJECTS = {} # a eid and set(object obejct) pair


EVENT_ID_COUNT = 0


def register_event(eid: int):
    """Register an event ID - just an integer value"""
    global REGISTERED_EVENTS, REGISTERED_OBJECTS
    # create registries within the dicts
    REGISTERED_EVENTS[eid] = EventRegistry(eid)
    REGISTERED_OBJECTS[eid] = set()
    return eid


def register_func_to_event(eid, func):
    """Register a function/object to an event"""
    global REGISTERED_OBJECTS
    # if not registered, register the event
    if REGISTERED_OBJECTS.get(eid) == None: 
        raise RegistryNotFound(eid)
    # register the event now
    REGISTERED_OBJECTS[eid].add(func)


def call_event(eid, data):
    """Call all functions registered into the eid"""
    global REGISTERED_OBJECTS, REGISTERED_EVENTS
    for e in REGISTERED_OBJECTS[eid]:
        # registered objects
        e(data)


class EventDataBlock:
    def __init__(self, eid, data):
        """Constructor for event data block"""
        self.eid = eid
        self.data = data


class EventRegistry:
    def __init__(self, eid):
        """Event ID - only holds the eid - probably bad memory management lol"""
        self.eid = eid


class Event:
    def __init__(self, data: dict, eid=0):
        """Event constructor"""
        self.data = data
        self.eid = eid if eid > 0 else Event.gen_event_id()
    
    @classmethod
    def gen_event_id(cls):
        """Generate Event ID classmethod"""
        global EVENT_ID_COUNT
        EVENT_ID_COUNT += 1
        return EVENT_ID_COUNT



# ------------ error ---------------- #
class RegistryNotFound(Exception):
    def __init__(self, eid):
        super().__init__(f"Event ID {eid} does not exist!")

