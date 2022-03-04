import pygame
from bin.game import worldgeneration


pygame.init()

# basic biome
Simplex = worldgeneration.WorldGenerator(1)
Biome = worldgeneration.Biome()

window = pygame.display.set_mode([1280, 720], 0, 32)
clock = pygame.time.Clock()

WIDTH = 40
HEIGHT = 40


def get_chunk(x, y):
    l = WIDTH * x
    t = HEIGHT * y
    biome_data = []
    for y in range(WIDTH):
        for x in range(HEIGHT):
            biome_data.append(Biome.filter2d(Simplex, (x+l) / WIDTH, (y+t) / HEIGHT))
    return biome_data


def render_biome(window, biome, width, height, w, h, left, top):
    col = (127, 127, 127)
    for y in range(height):
        for x in range(height):
            b = biome[y * height + x] + 1
            c = list(map(lambda x: int(x*b), (col[0], col[1], col[2])))
            pygame.draw.rect(window, c, (left + x * w, top + y * h, w, h))


b1 = get_chunk(1,1)
b2 = get_chunk(2,1)

run = True
while run:
    # window.fill((255,255,255))
    render_biome(window, b1, WIDTH, HEIGHT, 4, 4, 50, 50)
    render_biome(window, b2, WIDTH, HEIGHT, 4, 4, 50 + WIDTH * 4, 50)
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    clock.tick(30)

pygame.quit()

