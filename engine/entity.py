from . import filehandler

object_count = 0

def create_object_id():
    global object_count
    object_count += 1
    return object_count


class object:
    def __init__(self):
        self.id = create_object_id()


class Entity(object):
    def __init__(self):
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
        self.c_move = [0, 0]

    def update(self, dt):
        pass

    def render(self, window):
        window.blit(self.image, self.pos)


def set_entity_properties(x, y, w, h, img, entity):
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


