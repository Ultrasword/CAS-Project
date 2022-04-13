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

# ------- Serialize chunks ------------- #

class SerializeChunk(Serializable):
    def __init__(self):
        """Serialize chunks"""
        
        pass


