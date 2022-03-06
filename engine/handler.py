from collections import deque


class Handler:
    def __init__(self):
        # entities
        self.entities = {}
        self.active_entites = deque()

        # world
        self.world = {}
        self.active_chunks = deque()
    
    def add_entity(self, entity):
        self.entities[entity.id] = entity
    
    def add_chunk(self, chunk):
        self.world[chunk.id] = chunk
    
    def update_and_render_entities(self, window, dt, offset):
        for entity in self.entities.values():
            entity.update(dt)
            entity.render(window, offset)
    
    def render_chunks(self, window, offset):
        for a in self.active_chunks:
            self.world[a].render_grid(window, offset)
            self.world[a].render_blocks(window, offset)

