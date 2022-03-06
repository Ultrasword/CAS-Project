from . import filehandler

from collections import deque

CHUNK_WIDTH = 16
CHUNK_HEIGHT = 16
# x, y, w, h, img is a string
BLOCK_DATA_LENGTH = 6
# x, y, img
TILE_DATA_LENGTH = 4

TILE_WIDTH = 32

BLOCK_X = TILE_X = 0
BLOCK_Y = TILE_Y = 1
BLOCK_W = TILE_I = 2
BLOCK_H = TILE_HIT = 3
BLOCK_I = 4
BLOCK_HIT = 5

CHUNK_BLOCK_COUNT = 256

class Chunk:
    def __init__(self, x:int, y:int, tilegrid:list = [], blocks:list = []):
        """Create chunk - stores blocks and the environment"""
        # chunk position
        self.id = f"{x}.{y}"
        self.pos = (x, y)
        self.offset = (x*TILE_WIDTH*CHUNK_WIDTH, y*TILE_WIDTH*CHUNK_HEIGHT)
        # grid - for placing blocks :D
        self.grid = [[0 for i in range(TILE_DATA_LENGTH)] for i in range(CHUNK_WIDTH * CHUNK_HEIGHT)]
        for d in tilegrid:
            index = d[1] * CHUNK_WIDTH + d[0]
            for i in range(TILE_DATA_LENGTH):
                self.grid[index][i] = data[i]
        # blocks
        self.blocks = []
    
    def render_grid(self, window, offset):
        """Renders the chunk tilegrid"""
        for tile in self.grid:
            if tile[TILE_I]:
                window.blit(filehandler.get_image(tile[TILE_I]), (tile[TILE_X]*TILE_WIDTH + offset[0] + self.offset[0],
                    tile[TILE_Y]*TILE_WIDTH + offset[1] + self.offset[1]))

    def render_blocks(self, window, offset):
        """Renders the chunk blocks"""
        for block in self.blocks:
            if block[BLOCK_I]:
                window.blit(filehandler.get_image(block[BLOCK_I]), (block[BLOCK_X] + offset[0] + self.offset[0],
                        block[BLOCK_Y] + offset[1] + self.offset[1]))

    def set_tile_at(self, x, y, tile):
        """set tile at a certian x y position - position is relative to the chunk"""
        index = tile[1] * CHUNK_WIDTH + tile[0]
        for i in range(TILE_DATA_LENGTH):
            self.grid[index][i] = tile[i]


def create_block(x, y, img, w, h, collidable=0):
    """Create a block"""
    return (x, y, w, h, img, collidable)


def create_tile(x, y, img, collidable=0):
    """Create a tile"""
    return (x, y, img, collidable)
