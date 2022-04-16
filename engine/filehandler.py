import pygame

# pygame flags
SRC_ALPHA = pygame.SRCALPHA

# TODO - design a resizing system when loading images

images = {}

def get_image(img):
    """get and image"""
    if not images.get(img):
        if img.endswith(".png"):
            image = pygame.image.load(img).convert_alpha()
        else:
            image = pygame.image.load(img).convert()
        images[img] = image
    return images[img]


def get_image_without_cache(img):
    """get image wihtout cache or convert"""
    if img.endswith(".png"):
        return pygame.image.load(img).convert_alpha()
    return pygame.image.load(img).convert()


def scale(img, size):
    """scale images"""
    return pygame.transform.scale(img, size)


def xflip(img):
    """flips image across y axis"""
    return pygame.transform.flip(img, True, False)


def yflip(img):
    """flips image across x axis"""
    return pygame.transform.flip(img, False, True)


def make_surface(width, height, flags=0):
    """Make a surface object and return it"""
    return pygame.Surface((width, height), flags).convert_alpha()


def crop_image(source, target, source_area):
    """Crop source onto target given areas"""
    target.blit(source, (0, 0), source_area)

