import pygame


images = {}


def get_image(img):
    if not images.get(img):
        image = pygame.image.load(img).convert()
        images[img] = image
    return images[img]


