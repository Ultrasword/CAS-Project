import pygame
from engine import filehandler, window


# chunks will have a set size of 12 x 12
CHUNK_WIDTH = CHUNK_HEIGHT = 12
CHUNK_TILE_WIDTH = CHUNK_TILE_HEIGHT = 64
CHUNK_WIDTH_PIX = CHUNK_WIDTH * CHUNK_TILE_WIDTH
CHUNK_HEIGHT_PIX = CHUNK_HEIGHT * CHUNK_TILE_HEIGHT
CHUNK_TILE_AREA = (CHUNK_TILE_WIDTH, CHUNK_TILE_HEIGHT)

TILE_X = 0
TILE_Y = 1
TILE_IMG = 2
TILE_COL = 3


class Chunk:
    def __init__(self, pos: tuple):
        """Chunk Constructor"""
        self.chunk_id = pos[0] + (pos[1] << 16)
        self.pos = (pos[0], pos[1])
        self.world_pos = (pos[0] * CHUNK_WIDTH_PIX, pos[1] * CHUNK_HEIGHT_PIX)

        # images are all references cuz python only uses refs
        self.images = {}

        # visual aspects
        self.tile_map = tuple(tuple(Chunk.create_grid_tile(x, y, None) for x in range(CHUNK_WIDTH)) for y in range(CHUNK_HEIGHT))

    @property
    def id(self) -> int:
        """get the chunk id pos"""
        return self.chunk_id
    
    @staticmethod
    def create_grid_tile(x: int, y: int, img: str, collide: int = 0) -> list:
        """
        Create a tile object
        
        The position from (x, y) is converted to 
                (x * TILE_WIDTH + self.world_pos[0], y * TILE_HEIGHT + self.world_pos[1])
        
        This ensures unecassary calculations are not performed
        """
        return [x, y, img, 1]
                        
    def set_tile_at(self, tile: list) -> None:
        """Set a tile at - get the tile data from Chunk.create_grid_tile()"""
        if not self.images.get(tile[TILE_IMG]):
            # load the image - with the img size
            self.images[tile[TILE_IMG]] = filehandler.scale(filehandler.get_image(tile[TILE_IMG]), CHUNK_TILE_AREA)
        # set the data in the cache
        x, y = tile[TILE_X], tile[TILE_Y]
        self.tile_map[y][x][TILE_X] = x * CHUNK_TILE_WIDTH + self.world_pos[0]
        self.tile_map[y][x][TILE_Y] = y * CHUNK_TILE_HEIGHT + self.world_pos[1]
        self.tile_map[y][x][TILE_IMG] = tile[TILE_IMG]
        self.tile_map[y][x][TILE_COL] = tile[TILE_COL]

    def render(self, offset: tuple = (0, 0)) -> None:
        """Renders all the grid tiles and non tile objects"""
        for x in range(CHUNK_WIDTH):
            for y in range(CHUNK_HEIGHT):
                # get block data
                block = self.tile_map[y][x]
                if block[TILE_IMG]:
                    # render
                    window.FRAMEBUFFER.blit(self.images[block[TILE_IMG]], (block[TILE_X] + offset[0], block[TILE_Y] + offset[1]))


class World:
    def __init__(self):
        """World Constructor"""
        self.chunks = {}
        
        # args
        self.r_distance = 2
        
    def add_chunk(self, chunk: Chunk) -> None:
        """add a chunk to the world"""
        self.chunks[chunk.chunk_id] = chunk
    
    def make_template_chunk(self, x: int, y: int) -> Chunk:
        """Make a default empty chunk"""
        self.chunks[x + (y << 16)] = Chunk((x, y))
        return self.chunks[x + (y << 16)]
    
    def get_chunk(self, x: int, y: int) -> Chunk:
        """Get chunk from the world chunk cache"""
        return self.chunks.get(x + (y << 16))
    
    def render_chunks(self, rel_center: tuple, offset: tuple = (0, 0)) -> None:
        """Render the world with the set render distance | include a center"""
        for cx in range(rel_center[0] - self.render_distance, rel_center[0] + self.render_distance + 1):
            for cy in range(rel_center[1] - self.render_distance, rel_center[1] + self.render_distance + 1):
                if self.get_chunk(cx, cy):
                    self.get_chunk(cx, cy).render(offset)
    
    @property
    def render_distance(self) -> int:
        """Return render distance"""
        return self.r_distance
    
    @render_distance.setter
    def render_distance(self, new: int) -> int:
        """Set render distance"""
        self.r_distance = new


