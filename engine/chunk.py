from . import filehandler, maths, draw, tile as engine_tile

from collections import deque

CHUNK_WIDTH = 8
CHUNK_HEIGHT = 8
# x, y, w, h, img is a string
BLOCK_DATA_LENGTH = 6
# x, y, img
TILE_DATA_LENGTH = 4

TILE_WIDTH = 128

BLOCK_X = TILE_X = 0
BLOCK_Y = TILE_Y = 1
BLOCK_W = TILE_I = 2
BLOCK_H = TILE_HIT = 3
BLOCK_I = 4
BLOCK_HIT = 5

CHUNK_BLOCK_COUNT = CHUNK_WIDTH * CHUNK_HEIGHT
CHUNK_WIDTH_PIX = CHUNK_HEIGHT_PIX = TILE_WIDTH * CHUNK_WIDTH

WORLD_BORDER = 1000

# debug draw
DEBUG_COLOR = (255,0,0)


class Chunk:
    def __init__(self, x:int, y:int, tilegrid:list = [], blocks:list = []):
        """Create chunk - stores blocks and the environment"""
        self.pos = [x * CHUNK_WIDTH_PIX, y * CHUNK_HEIGHT_PIX]
        self.area = [CHUNK_WIDTH_PIX, CHUNK_HEIGHT_PIX]
        
        # chunk position
        self.id = maths.two_hash(x, y)                               # the id is a hash
        self.pos = (x, y)
        self.offset = (x*TILE_WIDTH*CHUNK_WIDTH, y*TILE_WIDTH*CHUNK_HEIGHT)
        
        # grid - for placing blocks :D
        self.grid = [[0 for i in range(TILE_DATA_LENGTH)] for i in range(CHUNK_BLOCK_COUNT)]
        for d in tilegrid:
            # get index
            index = d[1] * CHUNK_WIDTH + d[0]
            # check if the image directory is an actual image or an image name
            if engine_tile.get_tile_key(d[TILE_I]):
                # if it is an actual image, then turn it into an image name
                d[TILE_I] = engine_tile.get_tile_key(d[TILE_I])
            # set data into tilegrid index
            for i in range(TILE_DATA_LENGTH):
                self.grid[index][i] = d[i]
        # blocks
        self.blocks = []
    
    def render_grid(self, window, offset):
        """Renders the chunk tilegrid"""
        for tile in self.grid:
            if tile[TILE_I]:
                window.blit(engine_tile.get_tile(tile[TILE_I]).image, (tile[TILE_X]*TILE_WIDTH + offset[0] + self.offset[0],
                    tile[TILE_Y]*TILE_WIDTH + offset[1] + self.offset[1]))

    def render_blocks(self, window, offset):
        """Renders the chunk blocks"""
        for block in self.blocks:
            if block[BLOCK_I]:
                window.blit(filehandler.get_image(block[BLOCK_I]), (block[BLOCK_X] + offset[0] + self.offset[0],
                        block[BLOCK_Y] + offset[1] + self.offset[1]))

    def debug_render(self, window, offset):
        for i in range(CHUNK_BLOCK_COUNT):
            # render it
            tile = self.grid[i]
            if not tile[TILE_HIT]:
                continue
            draw.DEBUG_DRAW_LINE(window, DEBUG_COLOR,
                (tile[0] * TILE_WIDTH, tile[1] * TILE_WIDTH),
                (tile[0] * TILE_WIDTH + TILE_WIDTH, tile[1] * TILE_WIDTH + TILE_WIDTH)
            )

    def set_tile_at(self, tile):
        """set tile at a certian x y position - position is relative to the chunk"""
        index = tile[0] * CHUNK_WIDTH + tile[1]
        
        # set tile and then get name
        # if the tile image string is a directory path, convert to image name
        if engine_tile.get_tile_key(tile[TILE_I]):
            tile[TILE_I] = engine_tile.get_tile_key(tile[TILE_I])

        # now set all the indices in the place correcto yay
        for i in range(TILE_DATA_LENGTH):
            self.grid[index][i] = tile[i]
    
    def get_tile_at(self, x, y):
        return self.grid[x * CHUNK_WIDTH + y]
    
    def entity_overlap(self, entity):
        if self.pos[0] > entity.pos[0] + entity.hitbox[0] + entity.hitbox[2]:
            return False
        if self.pos[1] > entity.pos[1] + entity.hitbox[1] + entity.hitbox[3]:
            return False
        if self.pos[0] + self.area[0] < entity.pos[0] + entity.hitbox[0]:
            return False
        if self.pos[1] + self.area[1] < entity.pos[1] + entity.hitbox[1]:
            return False
        return True

    def get_colliding_tiles(self, entity):
        """Returns the ranges for colliding blocks"""
        # get all tiles the entity collides with
        # get relative to chunk
        relx = int(entity.pos[0] + entity.hitbox[0] - self.offset[0])
        rely = int(entity.pos[1] + entity.hitbox[1] - self.offset[1])

        # find the tile position
        left = maths.clamp(relx // TILE_WIDTH, 0, CHUNK_WIDTH)
        right = maths.clamp((relx + entity.hitbox[2]) // TILE_WIDTH + 1, 0, CHUNK_WIDTH)
        top = maths.clamp(rely // TILE_WIDTH, 0, CHUNK_HEIGHT)
        bottom = maths.clamp((rely + entity.hitbox[3]) // TILE_WIDTH + 1, 0, CHUNK_HEIGHT)
        return (left, right, top, bottom)

    def collide_and_move_x(self, entity, cols):
        """Collides only on x axis"""
        valx = round(entity.motion[0])
        for x in range(cols[0], cols[1]):
            for y in range(cols[2], cols[3]):
                tile = self.get_tile_at(x, y)
                # print(tile)
                if not tile[TILE_HIT]:
                    continue
                if collide_tile(entity, tile):
                    if valx > 0:
                        # moving right
                        entity.pos[0] = tile[TILE_X] * TILE_WIDTH - entity.hitbox[2] - entity.hitbox[0] - 1
                        entity.motion[0] = 0
                    elif valx < 0:
                        # moving left
                        entity.pos[0] = tile[TILE_X] * TILE_WIDTH + TILE_WIDTH - entity.hitbox[0]
                        entity.motion[0] = 0
    
    def collide_and_move_y(self, entity, cols):
        """Collides only on y axis"""
        valy = round(entity.motion[1])
        for x in range(cols[0], cols[1]):
            for y in range(cols[2], cols[3]):
                tile = self.get_tile_at(x, y)
                # print(tile)
                if not tile[TILE_HIT]:
                    continue
                if collide_tile(entity, tile):
                    # check y now cuz why not
                    if valy > 0:
                        # moving down
                        entity.pos[1] = tile[TILE_Y] * TILE_WIDTH - entity.hitbox[3] - entity.hitbox[1] - 1
                        entity.motion[1] = 0
                    elif valy < 0:
                        # moving up
                        entity.pos[1] = tile[TILE_Y] * TILE_WIDTH + TILE_WIDTH - entity.hitbox[1]
                        entity.motion[1] = 0


def create_block(x, y, img, w, h, collidable=0):
    """Create a block"""
    return (x, y, w, h, img, collidable)


def create_tile(x, y, img, collidable=0):
    """Create a tile"""
    return [x, y, img, collidable]


def collide_tile(entity, obj):
    """Perform collisions between entitys and [tiles]"""
    ol = obj[0] * TILE_WIDTH
    ot = obj[1] * TILE_WIDTH
    if entity.hitbox[0] + entity.pos[0] > ol +  TILE_WIDTH:
        return False
    if entity.hitbox[0] + entity.hitbox[2] + entity.pos[0] < ol:
        return False
    if entity.hitbox[1] + entity.pos[1] > ot + TILE_WIDTH:
        return False
    if entity.hitbox[1] + entity.hitbox[3] + entity.pos[1] < ot:
        return False
    return True

