import json
import os

from . import filehandler


TILE_ID_COUNT = 0
TILE_WIDTH = 0

def gen_tile_id():
    """Generate tile ID"""
    global TILE_ID_COUNT
    TILE_ID_COUNT += 1
    return TILE_ID_COUNT


TILE_FILE_EXT = ".tef"

file_to_key = {}
loaded_tiles = {}


def init_tiles(folder):
    """Initialize all .tef files"""
    for file in os.listdir(folder):
        if not file.endswith(TILE_FILE_EXT):
            continue
        path = os.path.join(folder, file)
        # if the file is a folder, then recursion
        if os.path.isdir(path):
            init_files(path)
        # if not a folder, then load tile
        add_tile(path)


def get_tile_key(name):
    """Get the tile name given a filepath"""
    return file_to_key.get(name)


def get_tile(key):
    """Get a tile given a name"""
    return loaded_tiles.get(key)


def add_tile(tile_data_path):
    """Add a tile to the loaded tiles"""
    with open(tile_data_path, 'r') as file:
        data = json.load(file)
        file.close()
    name = data["name"]
    friction = data["friction"]
    image = filehandler.scale(filehandler.get_image_without_cache(data["image"]), (TILE_WIDTH, TILE_WIDTH))
    loaded_tiles[name] = Tile(name, image, friction=friction)
    file_to_key[data["image"]] = name


class Tile:
    def __init__(self, name, image, friction=-1):
        """Tile constructor"""
        self.id = gen_tile_id()
        self.image = image
        self.name = name
        self.friction = friction
