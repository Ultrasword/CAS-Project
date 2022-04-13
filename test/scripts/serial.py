from engine.globals import *
from engine import world, serialize


SC = serialize.SerializeChunk()

C = world.Chunk((0,0))

print(SC.serialize(C))

