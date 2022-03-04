import pygame
import os

LOADED_IMAGES = {}


LOADED = {}
FONT = {}


# img size decode
def size_to_num(size):
    return (size[0] << 8) + size[1]


def num_to_size(num):
    return [(w := (num >> 8) - 1), num - (w < 8)]


def load_loaded_image(img, sizenum):
    return LOADED[sizenum][img]


def has_image(img, size):
    s = size_to_num(size)
    r = LOADED.get(s)
    if not r:
        get_image(img, size)
    elif not r.get(img):
        get_image(img, size)


def get_image(path, size=None):
    # CHECK IF FILE EXISTS
    if not os.path.exists(path):
        raise Exception(f"File does not exist at {path}")

    # load image
    image = pygame.image.load(path).convert_alpha()

    # check if there is a specified size
    if size:
        bytesize = size_to_num(size)
        # add the new size to LOADED
        image = pygame.transform.scale(image, size)
    else:
        # get image size
        size = image.get_size()
        # get bytesize
        bytesize = size_to_num(size)
    # ADD TO LOADED
    if not LOADED.get(bytesize):
        LOADED[bytesize] = {path: image}
    else:
        LOADED[bytesize][path] = image
    # return image
    return pygame.transform.scale(image, size)


def load_font(font, size=32):
    # check if size exists
    if not FONT.get(size):
        FONT[size] = {}
    # check if font already loaded
    if not FONT[size].get(font):
        FONT[size][font] = pygame.font.Font(font, size)
    return FONT[size][font]


def resize(img, size):
    return pygame.transform.scale(img, size).convert_alpha()


def load_animation_from_sprite_sheet(path, width, height, frames, x_off, y_off):
    # open the image file and cut out the areas for frames
    # print(path)
    sprite_sheet = get_image(path)
    frame_data = []
    sheet_width = sprite_sheet.get_width()
    sheet_height = sprite_sheet.get_height()
    img_dimensions = (width, height)
    x_section = width + 2 * x_off
    y_section = height + 2 * y_off

    # loop through until reach the end of the sprite sheet
    count = 0
    for y in range(0, sheet_height // x_section):
        for x in range(0, sheet_width // y_section):
            # check if out of range
            if count >= frames:
                return frame_data

            # load the new image
            rect = pygame.Rect(x_off + x_section * x,
                               y_off + y_section * y,
                               width, height)

            # rect = pygame.Rect(x * width, y * height, width, height)
            img = pygame.Surface(img_dimensions, flags=pygame.SRCALPHA, depth=32)
            img.blit(sprite_sheet, (0, 0), rect)

            frame_data.append(img)
            count += 1

    return frame_data
