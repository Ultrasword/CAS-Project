import pygame
import pickle
import json
import random
import numpy as np

from PIL import Image as PIL_Image

from bin.engine import taskqueue, handler, state
from bin.engine.multiprocesshandling import PROCESS_SHARED_ARRAY_SPACE
from bin.engine.filehandler import size_to_num
from bin import maths


TASK_OBJECT = taskqueue.Task

with open("assets/environment/env.json", 'r') as file:
    ENVIRONMENT_DATA = json.load(file)
    file.close()


class EndProcess:
    def __init__(self, shared_memory, data):
        """For end game - its just so that the function runs"""
        pass

    def run(self, send, uid):
        send.send((EndProcess, ()))


class LoadChunk(TASK_OBJECT):
    ENV_LIMIT = 10

    def __init__(self, shared_memory, data):
        """For loading chunks"""
        super(LoadChunk, self).__init__(shared_memory)
        # data = [biome, simplex, chunk_pos]
        self.biome = data[0]
        self.simplex = data[1]
        self.pos = data[2]
        self.e_count = 0
        # print(self.pos)
        # i want chunks to load layer by layer
        self.width = handler.CHUNK_BLOCK_WIDTH
        self.height = handler.CHUNK_BLOCK_HEIGHT
        self.chunk_str = ".".join([str(x) for x in self.pos])
        self.terrain = np.ndarray((self.width, self.height, 3))
        self.env = [0 for i in range(LoadChunk.ENV_LIMIT)]

    def run(self, send, uid):
        l = self.width * self.pos[0]
        t = self.height * self.pos[1]
        ll = self.pos[0] * handler.CHUNK_SIZE_PIX
        tt = self.pos[1] * handler.CHUNK_SIZE_PIX
        # create texture for the ground
        # create the height map, tile map, and empty for now
        for y in range(self.height):
            for x in range(self.width):
                value = self.biome.filter2d(self.simplex, (x + l) / self.width, (y + t) / self.height)
                # store
                self.terrain[x][y] = self.biome.color_func(value)
                # store the height level and also calculate the good environment to place
                self.calc_environment(value, x, y, ll, tt)
        send.send((self.result, self.chunk_str, self.terrain, self.env))
        # print("loaded chunk ", self.pos)

    @staticmethod
    def result(world, args):
        chunk = world.get_chunk(args[0], auto_start=False)
        if chunk:
            chunk.raw_terrain = pygame.surfarray.make_surface(args[1])
            chunk.terrain = pygame.transform.scale(chunk.raw_terrain,
                                        (handler.CHUNK_SIZE_PIX, handler.CHUNK_SIZE_PIX)).convert_alpha()
            # add enviroment stuff
            for e in args[2]:
                if e:
                    chunk.add_block(e)

    def calc_environment(self, value, x, y, l, t):
        if self.e_count >= self.ENV_LIMIT:
            return
        h = (value+1) * 127
        add = random.random()
        if add > 0.2:
            return
        # if greater than water level and sand level
        if h > 120:
            # random to check if you should add a rock or tree
            item = random.choice(ENVIRONMENT_DATA["types"])
            if item is None:
                return
            img = random.choice(ENVIRONMENT_DATA[item]["paths"])
            sx, sy = random.choice(ENVIRONMENT_DATA[item]["size"])
            self.env[self.e_count] = (ENVIRONMENT_DATA["folder"]+img, l+x*handler.BLOCK_SIZE, t+y*handler.BLOCK_SIZE,
                                      sx, sy, size_to_num((sx, sy)))
            self.e_count += 1


class SaveChunkData(TASK_OBJECT):
    def __init__(self, shared_memory, data):
        """For saving chunks to cache"""
        super(SaveChunkData, self).__init__(shared_memory)
        self.directory = data[0]
        self.x = data[1]
        self.y = data[2]
        self.raw_terrain_image = data[3]
        self.size = data[4]

    def run(self, send, uid):
        pil_image = PIL_Image.frombytes("RGBA", self.size,
                                        self.raw_terrain_image)
        pil_image.save(f"{self.directory}/{self.x}.{self.y}.png")
        send.send((self.result, f"{self.x}.{self.y}", f"{self.directory}/{self.x}.{self.y}.png"))
        # print("cached chunk ", self.x, self.y)

    @staticmethod
    def result(world, args):
        # we want to clear the chunk image data
        chunk = world.get_chunk(args[0], create=False)
        if chunk:
            chunk.terrain = None
            chunk.raw_terrain = None
            world.cached_chunks[args[0]] = args[1]


class LoadCacheChunk(TASK_OBJECT):
    def __init__(self, shared_memory, data):
        """For loading cached chunks"""
        super(LoadCacheChunk, self).__init__(shared_memory)
        self.directory = data[0]
        self.x = data[1]
        self.y = data[2]

    def run(self, send, uid):
        # load image using pygame
        img = pygame.image.load(f"{self.directory}/{self.x}.{self.y}.png")
        raw_terrain_image = pygame.image.tostring(img,
                                                  "RGBA", False)
        send.send((self.result, f"{self.x}.{self.y}", raw_terrain_image, img.get_size()))
        print("cache load chunk ", self.x, self.y)

    @staticmethod
    def result(world, args):
        chunk = world.get_chunk(args[0], create=False)
        if chunk:
            chunk.raw_terrain = pygame.image.fromstring(args[1], args[2], "RGBA", False)
            chunk.terrain = pygame.transform.scale(chunk.raw_terrain,
                                            (handler.CHUNK_SIZE_PIX, handler.CHUNK_SIZE_PIX))


class ShrinkChunkSize(TASK_OBJECT):
    def __init__(self, shared_memory, data):
        """Instead of unloading the entire terrain, unload the scaled image and store the raw terrain image"""
        super(ShrinkChunkSize, self).__init__(shared_memory)
        self.p_string = data[0]

    def run(self, send, uid):
        # offload the scaled image
        send.send((self.result, self.p_string))

    @staticmethod
    def result(world, args):
        chunk = world.get_chunk(args[0], create=False)
        if chunk:
            chunk.terrain = None
            world.cached_chunks[args[0]] = True


class ResizeChunkTerrain(TASK_OBJECT):
    def __init__(self, shared_memory, data):
        """Instead of unloading the entire terrain, unload the scaled image and store the raw terrain image"""
        super(ResizeChunkTerrain, self).__init__(shared_memory)
        self.p_string = data[0]

    def run(self, send, uid):
        # offload the scaled image
        send.send((self.result, self.p_string))

    @staticmethod
    def result(world, args):
        chunk = world.get_chunk(args[0], create=False)
        if chunk:
            chunk.terrain = pygame.transform.scale(chunk.raw_terrain, (handler.CHUNK_SIZE_PIX, handler.CHUNK_SIZE_PIX))
