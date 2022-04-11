"""
File for object types in the engine
"""

# ---------------- dataclass --------------- #

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
        obj.pos[0] = self.x
        obj.pos[1] = self.y
        obj.area[0] = self.w
        obj.area[1] = self.h


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
        """Constructor for Object class"""
        # object identification
        self.object_id = 0

        # standard variables
        self.pos = [0.0, 0.0]
        self.area = [0.0, 0.0]

        # physics properties
        self.friction = [0.0, 0.0]
        self.motion = [0.0, 0.0]

    @property
    def id(self):
        """Get the object id"""
        return self.object_id
    
    def update(self, dt):
        """Default update method"""
        pass
    
    def handle_changes(self):
        """Default handle changes method"""
        pass
    
    def render(self):
        """Default render function"""
        pass

    @property
    def center(self):
        """Get's center of the object"""
        return (self.pos[0] + self.area[0] // 2, self.pos[1] + self.area[1] // 2)
    
    @property
    def left(self):
        """Get's left of object"""
        return self.pos[0]
    
    @property
    def right(self):
        """Get's right of object"""
        return self.pos[0] + self.area[0]
    
    @property
    def top(self):
        """Get's top of object"""
        return self.pos[1]
    
    @property
    def bottom(self):
        """Get's bottom of object"""
        return self.pos[1] + self.area[1]


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




