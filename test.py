import numpy as np


WIDTH = 300
HEIGHT = 300
DEPTH = 3

# terrain = np.ndarray((300, 300, 3), dtype=np.uint8)
# for i in range(300):
#     for j in range(300):
#         terrain[i][j][0] = 100
#         terrain[i][j][1] = 20
#         terrain[i][j][2] = 8
#
#
# print(terrain.nbytes)
#
# with open("file.chk", "wb") as file:
#     # write 10000 bytes at a time
#     data = terrain.tobytes()
#     times = terrain.nbytes // 10000
#     for i in range(times):
#         file.write(data[i*10000:(i+1)*10000+1])
#     if terrain.nbytes % 10000 != 0:
#         file.write(data[(i+1)*10000:])
#     file.close()


import pygame

# load data
with open("file.chk", "rb") as file:
    # just read everything idk
    data = file.read()
    # print(data)
    file.close()

terrain = np.ndarray((WIDTH, HEIGHT, DEPTH), dtype=np.uint8)
for i in range(WIDTH):
    for j in range(HEIGHT):
        l = i * WIDTH + j * HEIGHT
        d = tuple(np.uint8(x) for x in data[l:l+3])
        terrain[j][i] = d
        print(d, l)

# print(terrain)

pygame.init()

window = pygame.display.set_mode([1280, 720], 0, 32)
img = pygame.surfarray.make_surface(terrain).convert()
clock = pygame.time.Clock()

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    window.blit(img, (0,0))
    pygame.display.update()
    clock.tick(15)


