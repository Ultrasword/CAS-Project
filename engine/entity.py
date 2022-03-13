from . import filehandler

object_count = 0

def create_object_id():
    """generate unique global id"""
    global object_count
    object_count += 1
    return object_count


class object:
    def __init__(self):
        """object class Constructor"""
        self.id = create_object_id()


class Entity(object):
    def __init__(self):
        """Entity class Constructor"""
        super().__init__()
        
        # for collisions and stuff
        self.pos = [0, 0]
        self.area = [0, 0]
        #              xoff,    yoff    width, height
        self.hitbox = [0,       0,      0,    0]

        # image
        self.image = None
        self.image_offset = [0, 0]
        self.xflip = False

        # movement
        self.motion = [0, 0]

        # animation related things
        self.aid = 0
        self.state = None

    def update(self, dt):
        pass

    def render(self, window, offset):
        """Render entity"""
        window.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))

    def set_state(self, state):
        self.state = state
    
    def update_position(self):
        self.pos[0] += self.motion[0]
        self.pos[1] += self.motion[1]


def set_entity_properties(x, y, w, h, img, entity):
    """Set entity properties - position, area, img"""
    if x:
        entity.pos[0] = x
    if y:
        entity.pos[1] = y
    if w:
        entity.area[0] = w
    if h:
        entity.area[1] = h
    if img:
        entity.image = filehandler.get_image(img)

