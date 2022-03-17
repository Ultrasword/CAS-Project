"""
This module holds map loading functions
"""
import json
from engine import chunk


def create_tile_map(path):
    """Loads a tilemap made with tiled"""
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
    tex = data["textures"]
    world = data["world"]
    pos = data["pos"]
    c = chunk.Chunk(pos[0], pos[1])
    for i in range(chunk.CHUNK_WIDTH):
        for j in range(chunk.CHUNK_HEIGHT):
            g = world[i * chunk.CHUNK_WIDTH + j]
            c.set_tile_at([j, i, tex[g][0], tex[g][1]])
    return c


