from . import maths, chunk
from collections import deque


GRAVITY = 100


class Handler:
    def __init__(self):
        """Handler constructor"""
        # entities
        self.entities = {}
        self.active_entites = deque()

        # world
        self.world = {}
        self.active_chunks = deque()
    
    def add_entity(self, entity):
        """Add entity to the world"""
        self.entities[entity.id] = entity
    
    def add_chunk(self, chunk):
        """Add chunk to the world"""
        # the chunk id is a hash of the position
        self.world[chunk.id] = chunk
    
    def update_and_render_entities(self, window, dt, offset):
        """Update and render entities"""
        for entity in self.entities.values():
            entity.update(dt)
            if entity.moved:
                if entity.gravity:
                    entity.motion[1] += GRAVITY * dt
                self.move_entity(entity)
            entity.render(window, offset)
            # debug
            entity.debug_render(window, offset)
    
    def render_chunks(self, window, offset):
        """Render all active chunks"""
        for a in self.active_chunks:
            self.world[a].render_grid(window, offset)
            self.world[a].render_blocks(window, offset)
            # debug
            self.world[a].debug_render(window, offset)
    
    def move_entity(self, entity):
        """Move an entity and perform collision detection"""
        # calculate entity chunk
        entity.chunk[0] = int(entity.pos[0] // chunk.CHUNK_WIDTH_PIX)
        entity.chunk[1] = int(entity.pos[1] // chunk.CHUNK_HEIGHT_PIX)

        # TODO - redo the movement system
        entity.pos[0] += entity.motion[0]
        for x in range(entity.chunk[0] - 1, entity.chunk[0] + 2):
            for y in range(entity.chunk[1] - 1, entity.chunk[1] + 2):
                # chekc if if chunk exists
                c = self.world.get(maths.two_hash(x, y))
                if not c:
                    continue
                if not c.entity_overlap(entity):
                    continue
                c.collide_and_move_x(entity, c.get_colliding_tiles(entity))
        
        entity.pos[1] += entity.motion[1]
        for x in range(entity.chunk[0] - 1, entity.chunk[0] + 2):
            for y in range(entity.chunk[1] - 1, entity.chunk[1] + 2):
                # chekc if if chunk exists
                c = self.world.get(maths.two_hash(x, y))
                if not c:
                    continue
                # print(int(c.entity_overlap(entity)), c.pos, c.area, entity.pos, entity.area, entity.hitbox)
                if not c.entity_overlap(entity):
                    continue
                c.collide_and_move_y(entity, c.get_colliding_tiles(entity))

        entity.moved = False

