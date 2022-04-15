"""
Contains functions and methods for serializing level data

Serializable objects:
- Rect
- Animation
- Entity
- Chunk
- World
- Handler
- State

Output will be a .json file
Data can be loaded using the classes made in this file

"""

import json
import pickle

from engine.globals import *


# ------- Serialize base object -------- #

class Serializable:
    def __init__(self):
        """Serializable Constructor"""
        pass
    
    def serialize(self) -> dict:
        """Serialize the object"""
        return {}
    
    @staticmethod
    def save_to_file(file_path: str, data: dict) -> None:
        """Saves data to a .json file"""
        if not file_path.endswith(".json"):
            file_path += ".json"
        with open(file_path, "w") as file:
            json.dump(data, file) # indent=4)
            file.close()

# ------- Serialize chunks ------------- #

class SerializeChunk(Serializable):
    def __init__(self):
        """Serialize chunks"""
        super().__init__()

    def serialize(self, chunk) -> dict:
        """
        Serialize object
        
        chunk.images = {file path: pygame image object}
        - extract the image paths and convert to an integer

        """
        result = {}
        result[CHUNK_TILEMAP_KEY] = chunk.tile_map
        result[CHUNK_POS_KEY] = chunk.pos
        result[CHUNK_IMAGES_KEY] = {imid: val for imid, val in enumerate(chunk.images.keys())}
        return result


# ------- Serialize World -------------- #

class SerializeWorld(Serializable):
    def __init__(self):
        """Serialize world constructor"""
        super().__init__()

        self.chunk_serializer = SerializeChunk()

    def serialize(self, world) -> dict:
        """
        Serialize World

        - serializes all chunks contained within the world
        - important keys
            - chunks
        """
        result = {}
        result[WORLD_CHUNK_KEY] = [self.chunk_serializer.serialize(chunk) for _, chunk in world.chunks.items()]
        return result


# --------- Serialize Animation --------- #

class SerializeAnimation(Serializable):
    def __init__(self):
        """Serialize Animation constructor"""
        super().__init__()

    def serialize(self, animation_registry) -> dict:
        """
        Serialize Animation

        - gets the filepath and thats about it
        """
        result = {}
        result[ANIMATION_PATH_KEY] = animation_registry.handler.json_path
        result[ANIMATION_NAME_KEY] = animation_registry.handler.name
        return result


# --------- Serialize Entity ------------ #

class SerializeEntity(Serializable):
    def __init__(self):
        """Serialize Entity constructor"""
        super().__init__()

    def serialize(self, entity) -> dict:
        """
        Serialize Entity

        - rect data
        - animatino data | if it exists
        """
        result = {}
        # serialize the rect
        result[ENTITY_RECT_KEY] = entity.rect.serialize()
        # serialize animation
        result[ENTITY_ANIMATION_KEY] = None if not entity.ani_registry else entity.ani_registry.handler.name
        # serialize the entity type
        result[ENTITY_TYPE_KEY] = str(pickle.dumps(type(entity), protocol=4))
        return result


# --------- Serialize Handler ----------- #

class SerializeHandler(Serializable):
    def __init__(self):
        """Serialize handler construcstor"""
        super().__init__()

        self.entity_serializer = SerializeEntity()
        self.animation_serializer = SerializeAnimation()

    def serialize(self, handler) -> dict:
        """
        Serialize Handler
        - stores all entity data and serializes it
        - serializes the different animations as well :D
        """
        result = {}
        
        # find animations and entities
        animations = {}
        entities = {}
        for eid, entity in handler.p_objects.items():
            entities[eid] = self.entity_serializer.serialize(entity)
            # check if has an ani_registry
            if entity.ani_registry:
                block = self.animation_serializer.serialize(entity.ani_registry)
                animations[block[ANIMATION_NAME_KEY]] = block

        result[HANDLER_DATA_KEY] = entities
        result[HANDLER_ANIMATION_KEY] = animations
        return result


# --------- Serialize State -------------- #

class SerializeState(Serializable):
    def __init__(self):
        """Serialize State Constructor"""
        super().__init__()

        self.handler_serializer = SerializeHandler()
        self.world_serializer = SerializeWorld()


    def serialize(self, state) -> dict:
        """
        Serialize State

        - serialize the world and the handler
        - world will consists of
            - world.chunks = {}
        """
        
        result = {}
        
        # get handler data
        handler_data = self.handler_serializer.serialize(state)
        world_data = self.world_serializer.serialize(state)
        
        result[STATE_HANDLER_KEY] = handler_data
        result[STATE_WORLD_KEY] = world_data
        return result


