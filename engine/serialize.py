"""
Contains functions and methods for serializing level data

Serializable objects:
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
            json.dump(data, file)
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
        result[CHUNK_IMAGES_KEY] = {id: val for id, val in enumerate(chunk.images.keys())}
        return result


# ------- Serialize World -------------- #

class SerializeWorld(Serializable):
    def __init__(self):
        """Serialize World Constructor"""
        super().__init__()
    
    def serialize(self) -> dict:
        pass
 
