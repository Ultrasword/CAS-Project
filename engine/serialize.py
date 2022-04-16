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


# TODO - make a global image section for the json
# all the images will be stored there



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


# ------- Serialize tile --------------- #

class SerializeTile(Serializable):
    def __init__(self):
        """Serialize Tile constructor"""
        super().__init__()
    
    def serialize(self, tile, images) -> dict:
        """Serialize a tile given the image map"""
        pass

# ------- Serialize chunks ------------- #

class SerializeChunk(Serializable):
    def __init__(self):
        """Serialize chunks"""
        super().__init__()
        self.tile_serializer = SerializeTile()

    def serialize(self, chunk, images) -> dict:
        """
        Serialize object
        
        chunk.images = {file path: pygame image object}
        - extract the image paths and convert to an integer

        """
        result = {}
        # tile serializer?
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

    def serialize(self, world, images) -> dict:
        """
        Serialize World

        - serializes all chunks contained within the world
        - important keys
            - chunks
        """
        result = {}
        result[WORLD_CHUNK_KEY] = [self.chunk_serializer.serialize(chunk) for _, chunk in world.chunks.items()]
        return result


# --------- Serialize SpriteTile --------- #

class SerializeSpriteTile(Serializable):
    def __init__(self):
        """Serialize Sprite Tile constructor"""
        super().__init__()
        
    def serialize(self, tile) -> dict:
        """Serialize the tile dict"""
        result = {}
        # store the left, top, right, bottom of area on sprite sheet
        data = tile.sprite_data

        result[SPRITETILE_INDEX_KEY] = data.index
        result[SPRITETILE_RECT_KEY] = [data.x, data.y, data.w, data.h]
        result[SPRITETILE_PARENT_IMAGE_KEY] = data.parent_str

        return result

# --------- Serialize SpriteSheet --------- #

class SerializableSpriteSheet:
    def __init__(self):
        """Serializable SpriteSheet Constructor"""
        super().__init__()
        self.sprite_tile_serializer = SerializeSpriteTile()
    
    def serialize(self, sprite_sheet, images) -> dict:
        """Serialize the object"""
        result = {}
        result[SPRITESHEET_IMAGE_PATH_KEY] = sprite_sheet.sheet_path
        result[SPRITESHEET_SPRITES_KEY] = {}
        for tile in sprite_sheet.sprites:
            f = self.sprite_tile_serializer.serialize(tile)
            result[SPRITESHEET_SPRITE_KEY][f[SPRITETILE_INDEX_KEY]] = f

        result[SPRITESHEET_SPRITE_AREA_KEY] = list(sprite_sheet.sprite_area)
        result[SPRITESHEET_SPACING_KEY] = list(sprite_sheet.spacing)

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

    def serialize(self, handler, images) -> dict:
        """
        Serialize Handler
        - stores all entity data and serializes it
        - serializes the different animations as well :D

        - animations are stored not based on image path but json file
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
        result[HANDLER_ANIMATION_KEY] = animations # TODO - find a place to put animations
        return result


# --------- Serialize State -------------- #

class SerializeState(Serializable):
    def __init__(self):
        """Serialize State Constructor"""
        super().__init__()

        self.handler_serializer = SerializeHandler()
        self.world_serializer = SerializeWorld()
        self.sprite_sheet_serializer = SerializableSpriteSheet()


    def serialize(self, state) -> dict:
        """
        Serialize State

        - serialize the world and the handler
        - world will consists of
            - world.chunks = {}
        """
        
        result = {}
        result[STATE_IMAGES_KEY] = {}

        # get handler data
        handler_data = self.handler_serializer.serialize(state, result[STATE_IMAGES_KEY])
        world_data = self.world_serializer.serialize(state, result[STATE_IMAGES_KEY])
        
        result[STATE_HANDLER_KEY] = handler_data
        result[STATE_WORLD_KEY] = world_data
        return result


