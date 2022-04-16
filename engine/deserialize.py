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


# ------- Deserialize chunks ------------- #

class DeserializeChunk(Deserializable):
    def __init__(self):
        """Deserialize chunks"""
        super().__init__()

    def deserialize(self, chunk) -> world.Chunk:
        """
        Deserialize object
        
        chunk.images = {file path: pygame image object}
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


# ------- Deserialize World -------------- #
# TODO - implement rest #

class DeserializeWorld(Deserializable):
    def __init__(self):
        """Deserialize world constructor"""
        super().__init__()

        self.chunk_deserializer = DeserializeChunk()

    def deserialize(self, world) -> dict:
        """
        Deserialize World

        - deserializes all chunks contained within the world
        - important keys
            - chunks
        """
        result = world.World()
        # deserialize all chunks
        for chunk in world[WORLD_CHUNK_KEY]:
            result.add_chunk(self.chunk_deserializer.deserialize(chunk))
        return result


# --------- Deserialize Animation --------- #

class DeserializeAnimation(Deserializable):
    def __init__(self):
        """Deserialize Animation constructor"""
        super().__init__()

    def deserialize(self, animation_registry) -> dict:
        """
        Deserialize Animation

        - gets the filepath and thats about it
        """

        result = animation.create_animation_handler_from_json(animation_registry[ANIMATION_PATH_KEY])
        return result


# --------- Deserialize Entity ------------ #

class DeserializeEntity(Deserializable):
    def __init__(self):
        """Deserialize Entity constructor"""
        super().__init__()

    def deserialize(self, entity) -> dict:
        """
        Deserialize Entity

        - rect data
        - animatino data | if it exists
        """

        result = {}
        # deserialize the rect
        result[ENTITY_RECT_KEY] = entity.rect.deserialize()
        # deserialize animation
        result[ENTITY_ANIMATION_KEY] = None if not entity.ani_registry else entity.ani_registry.handler.name
        return result


# --------- Deserialize Handler ----------- #

class DeserializeHandler(Deserializable):
    def __init__(self):
        """Deserialize handler construcstor"""
        super().__init__()

        self.entity_deserializer = DeserializeEntity()
        self.animation_deserializer = DeserializeAnimation()

    def deserialize(self, handler) -> dict:
        """
        Deserialize Handler
        - stores all entity data and deserializes it
        - deserializes the different animations as well :D
        """
        result = {}
        
        # find animations and entities
        animations = {}
        entities = {}
        for eid, entity in handler.p_objects.items():
            entities[eid] = self.entity_deserializer.deserialize(entity)
            # check if has an ani_registry
            if entity.ani_registry:
                block = self.animation_deserializer.deserialize(entity.ani_registry)
                animations[block[ANIMATION_NAME_KEY]] = block

        result[HANDLER_DATA_KEY] = entities
        result[HANDLER_ANIMATION_KEY] = animations
        return result


# --------- Deserialize State -------------- #

class DeserializeState(Deserializable):
    def __init__(self):
        """Deserialize State Constructor"""
        super().__init__()

        self.handler_deserializer = DeserializeHandler()
        self.world_deserializer = DeserializeWorld()


    def deserialize(self, state) -> dict:
        """
        Deserialize State

        - deserialize the world and the handler
        - world will consists of
            - world.chunks = {}
        """
        
        result = {}
        
        # get handler data
        handler_data = self.handler_deserializer.deserialize(state)
        world_data = self.world_deserializer.deserialize(state)
        
        result[STATE_HANDLER_KEY] = handler_data
        result[STATE_WORLD_KEY] = world_data
        return result


