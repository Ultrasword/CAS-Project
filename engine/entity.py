from . import filehandler, chunk, maths, draw


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


DEBUG_COLOR = (0, 0, 0)


class Entity(object):
    def __init__(self):
        """Entity class Constructor"""
        super().__init__()
        
        # for collisions and stuff
        self.pos = [0, 0]
        self.area = [0, 0]
        self.chunk = [0, 0]
        #              xoff,    yoff    width, height
        self.hitbox = [0,       0,      0,    0]
        self.collided = [False, False, False, False]

        # image
        self.image = None
        self.image_offset = [0, 0]
        self.xflip = False
        self.flip_change = False

        # movement
        self.motion = [0, 0]
        self.moved = False
        self.gravity = False

        # animation related things
        self.aid = 0
        self.state = None

    def update(self, dt):
        pass

    def render(self, window, offset):
        """Render entity"""
        window.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))

    def debug_render(self, window, offset):
        draw.DEBUG_DRAW_LINE(window, DEBUG_COLOR, (self.hitbox[0] + self.pos[0], self.hitbox[1] + self.pos[1]),
                                 (self.pos[0] + self.hitbox[0] + self.hitbox[2], self.pos[1] + self.hitbox[1] + self.hitbox[3]))

    def set_state(self, state):
        self.state = state
    
    def update_position(self):
        self.pos[0] += self.motion[0]
        self.pos[1] += self.motion[1]
        self.chunk[0] = maths.mod(self.pos[0], chunk.CHUNK_WIDTH)
        self.chunk[1] = maths.mod(self.pos[1], chunk.CHUNK_HEIGHT)


def set_entity_properties(x, y, w, h, img, entity):
    """Set entity properties - position, area, img"""
    if x:
        entity.pos[0] = x
        entity.chunk[0] = maths.mod(entity.pos[0], chunk.CHUNK_WIDTH)
    if y:
        entity.pos[1] = y
        entity.chunk[1] = maths.mod(entity.pos[1], chunk.CHUNK_HEIGHT)
    if w:
        entity.area[0] = w
    if h:
        entity.area[1] = h
    if img:
        if entity.area[0] and entity.area[1]:
            entity.image = filehandler.scale(filehandler.get_image(img), entity.area)
        else:
            entity.image = filehandler.get_image(img)
