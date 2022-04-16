"""
File for object types in the engine
"""

# ---------------- dataclass --------------- #

from engine.globals import *
from dataclasses import dataclass

@dataclass
class ObjectData:
    """
    Used to hold data for setting object data
    """

    x: int
    y: int
    w: int
    h: int

    def set_object_params(self, obj) -> None:
        """Set property of objects below"""
        obj.rect.pos = self.x, self.y
        obj.rect.area = self.w, self.h

@dataclass
class Rect:
    """
    Holds position data and area data

    - pos [float, float]
    - area [float, float]

    Wow, amazing
    """

    x: float
    y: float
    w: float
    h: float

    # chunk pos
    cx: int = 0
    cy: int = 0

    def __init__(self, x: int, y: int, w: int, h: int):
        """Rect constructor"""
        self.x = x
        self.y = y
        self.w = w 
        self.h = h
        self.cx = self.x // CHUNK_WIDTH_PIX
        self.cy = self.y // CHUNK_HEIGHT_PIX

    def serialize(self):
        """Convert data to a dict"""
        return [self.x, self.y, self.w, self.h]
    
    @staticmethod
    def deserialize(self, data):
        """Deserialize data to create Rect"""
        return Rect(data[RECT_X_KEY], data[RECT_Y_KEY], data[RECT_W_KEY], data[RECT_H_KEY])

    @property
    def center(self):
        """Get's center of the object"""
        return (self.x + self.w // 2, self.y + self.h // 2)
    
    @property
    def left(self):
        """Get's left of object"""
        return self.x
    
    @property
    def right(self):
        """Get's right of object"""
        return self.x + self.w
    
    @property
    def top(self):
        """Get's top of object"""
        return self.y
    
    @property
    def bottom(self):
        """Get's bottom of object"""
        return self.y + self.h
    
    @property
    def topright(self):
        """Get top right"""
        return (self.x + self.w, self.y)
    
    @property
    def topleft(self):
        """Get top left"""
        return (self.x, self.y)
    
    @property
    def bottomright(self):
        """Get bottom right"""
        return (self.x + self.w, self.y + self.h)
    
    @property
    def bottomleft(self):
        """Get bottom left"""
        return (self.x, self.y + self.h)

    @property
    def width(self):
        """Get the width parameter"""
        return self.w
    
    @width.setter
    def width(self, other):
        """Set the width"""
        self.w = other

    @property
    def height(self):
        """Get the height parameter"""
        return self.h

    @height.setter
    def height(self, other):
        """Set the height parameter"""
        self.h = other

    @property
    def area(self):
        """Area getter"""
        return (self.w, self.h)

    @area.setter
    def area(self, a):
        """Area setter"""
        self.w = a[0]
        self.h = a[1]

    @property
    def pos(self):
        """Get the object position"""
        return (self.x, self.y)

    @pos.setter
    def pos(self, a):
        """Set the position"""
        self.x = a[0]
        self.y = a[1]
        self.cx = self.x // CHUNK_WIDTH_PIX
        self.cy = self.y // CHUNK_HEIGHT_PIX

    @property
    def chunk(self):
        """Return chunk pos"""
        self.cx = self.x // CHUNK_WIDTH_PIX
        self.cy = self.y // CHUNK_HEIGHT_PIX
        return (self.cx, self.cy)


@dataclass
class Touching:
    """
    Holds touching data
    
    Made for detecting if object edge is touching
    - I wish Python had Structs
    - not ctypes.Structure >:C
    """

    left: bool
    top: bool
    right: bool
    bottom: bool


# --------------- objects ---------------- #

ID_COUNTER = 0

def get_object_id():
    """get an object id"""
    global ID_COUNTER
    ID_COUNTER += 1
    return ID_COUNTER


class Object:
    """
    Defeault object class
    Has similar purpose to Persistent Object but acts as a non-persistent object class
    """

    def __init__(self):
        """
        Constructor for Object class
        
        Contains data:
            - object id: int
            - rect: Rect object
            - ani_registry: the Animation Registry object from animation.py
            - m_motion: list | holds x movement and y movement
            - touching: Touching object | determines if object is touching on each side of the rect
        """
        # object identification
        self.object_id = 0

        # standard variables - this is just the object rect 
        self.rect = Rect(0, 0, 0, 0)
        self.ani_registry = None

        # physics properties
        self.p_motion = [0.0, 0.0]
        self.m_motion = [0.0, 0.0]
        self.m_moving = [False, False]
        self.touching = Touching(False, False, False, False)

    @property
    def id(self):
        """Get the object id"""
        return self.object_id
    
    def update(self, dt: float) -> None:
        """Default update method"""
        pass
    
    def handle_changes(self):
        """Default handle changes method"""
        pass
    
    def render(self):
        """Default render function"""
        pass

    @property
    def animation(self):
        """Get the object animation registry"""
        return self.ani_registry
    
    @animation.setter
    def animation(self, other):
        """Set the animation"""
        self.ani_registry = other
    
    def update_animation(self, dt: float) -> None:
        """Updates the animation registry if it exists"""
        if self.ani_registry:
            self.ani_registry.update(dt)
            if self.ani_registry.changed:
                self.image = self.ani_registry.get_frame()


class PersistentObject(Object):
    """
    Objects are things that will be used to render in game entities
    they should not be used to create non-rendered objects

    Objects include:
    - entities
    - persistent effects

    Not include:
    - particles
    - background effects
    
    """
    def __init__(self):
        """ Constructor for Persistent Object class"""
        super().__init__()


# ------------------ handler ------------------ #

class Handler:
    """
    A persistent object and non persistent object handler
    When adding an object, you can either pick an specific type to add
    Or you can just use a default func defined

    Can add
    - entities
    - background effects
    - persistent background effects

    Should not add
    - Particles
    - should use ParticleHandler
    
    """
    def __init__(self):
        """Handler constructor"""
        # for persistent objects
        self.p_objects = {}

        # non persistent objects
        self.objects = {}
        self.non_p_object_counter = 0

        # updates
        self.dirty = True
    
    def get_non_persist_id(self):
        """Generate a non persisting id for this specific handler"""
        self.non_p_object_counter += 1
        return self.non_p_object_counter
    
    def add_persist_entity(self, entity):
        """Add persistent entity"""
        entity.object_id = get_object_id()
        self.p_objects[entity.id] = entity
    
    def add_non_persist_entity(self, entity):
        """Add non-persisting entity"""
        entity.object_id = self.get_non_persist_id()
        self.objects[entity.id] = entity
    
    def add_entity_auto(self, entity):
        """Add entity and auto select where it should go"""
        if isinstance(entity, PersistentObject):
            self.add_persist_entity(entity)
        else:
            self.add_non_persist_entity(entity)

    def remove_persistent_entity(self, eid):
        """Can only remove persistent entities"""
        if eid in self.p_objects:
            self.p_objects.pop(eid)
    
    def remove_entity(self, eid):
        """Can only remove non-persisting entities"""
        if eid in self.objects:
            self.objects.pop(eid)
        
    def handle_entities(self, dt):
        """
        Handle entities
        
        1. Update entities
            - pass through dt
        2. Render entities
            - pass through window
        """
        for eid, entity in self.p_objects.items():
            entity.update(dt)
            entity.handle_changes()
            entity.render()
        
        for eid, entity in self.objects.items():
            entity.update(dt)
            entity.handle_changes()
            entity.render()

    def render_all(self):
        """Render all entities in case needed to"""
        # usually used when window resized
        for eid, entity in self.p_objects.items():
            entity.dirty = True
            entity.render()
        
        for eid, entity in self.objects.items():
            entity.dirty = True
            entity.render()




