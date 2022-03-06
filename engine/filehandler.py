import pygame


# TODO - design a resizing system when loading images

images = {}

def get_image(img):
    if not images.get(img):
        image = pygame.image.load(img).convert()
        images[img] = image
    return images[img]


def scale(img, size):
    return pygame.transform.scale(img, size)


