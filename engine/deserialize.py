"""
Contains functions and methods + classes for deserializing level data

Deserialize objects:
- Rect
- Animation
- Entity
- Chunk
- World
- Handler
- State

Will return designated data types

"""

# ONLY STATE DATA CAN BE LOADED FROM .JSON


import json
import pickle

from engine.globals import *
from engine import handler, world, animation, filehandler, state


# ------- Deserialize base object -------- #

class Deserializable:
    def __init__(self):
        """Deserializable Constructor"""
        pass
    
    def deserialize(self) -> None:
        """Deserialize the object"""
        return


# ------- Deserialize 


# ------- Deserialize chunks ------------- #

class DeserializeChunk(Deserializable):
    def __init__(self):
        """Deserialize chunks"""
        super().__init__()

    def deserialize(self, chunk, spritesheets) -> world.Chunk:
        """
        Deserialize object
        
        chunk.images = {file path: pygame imawge object}
        - extract the image paths and convert to an integer

        """

        # TODO - add in compatibility for the SpriteSheet objects

        result = world.Chunk(chunk[CHUNK_POS_KEY])
        
        # create image cache for chunk
        for imid, path in chunk[CHUNK_IMAGES_KEY].items():
            result.images[path] = filehandler.scale(filehandler.get_image(path), world.CHUNK_TILE_AREA)
        
        # load all tile maps
        for x in range(CHUNK_WIDTH):
            for y in range(CHUNK_HEIGHT):
                tile = chunk[CHUNK_TILEMAP_KEY][y][x]
                result.set_tile_at(result.create_grid_tile(x, y, tile[TILE_IMG], tile[TILE_COL]))
        return result

