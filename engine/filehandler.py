import pygame


# TODO - design a resizing system when loading images

images = {}

def get_image(img):
    """get and image"""
    if not images.get(img):
        image = pygame.image.load(img).convert()
        images[img] = image
    return images[img]


def get_image_without_cache(img):
    """get image wihtout cache or convert"""
    return pygame.image.load(img).convert()


def scale(img, size):
    """scale images"""
    return pygame.transform.scale(img, size)


