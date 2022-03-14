import os
import json
import shutil

from . import window
from . import clock
from . import chunk
from . import tile


# load everything from settings.json
if not os.path.exists("assets"):
    os.mkdir("assets")

# if settings.json doesnt exist, create it
if not os.path.exists("assets/settings.json"):
    shutil.copy("engine/default_settings.json", "assets/settings.json")

# load everything from the files
with open("assets/settings.json", 'r') as file:
    data = json.load(file)
    file.close()


tile.TILE_FILE_EXT = data["TILE_FILE_EXT"]
tile.TILE_WIDTH = data["TILE_WIDTH"]

chunk.CHUNK_WIDTH = data["CHUNK_WIDTH"]
chunk.CHUNK_HEIGHT = data["CHUNK_HEIGHT"]
chunk.TILE_WIDTH = data["TILE_WIDTH"]
chunk.WORLD_BORDER = data["WORLD_BORDER"]
chunk.DEBUG_COLOR = tuple(data["DEBUG_COLOR"])

chunk.CHUNK_BLOCK_COUNT = chunk.CHUNK_WIDTH * chunk.CHUNK_HEIGHT
chunk.CHUNK_WIDTH_PIX = chunk.CHUNK_HEIGHT_PIX = chunk.TILE_WIDTH * chunk.CHUNK_WIDTH


