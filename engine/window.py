import pygame


# static variables
ORIGINAL_WIDTH, ORIGINAL_HEIGHT = 0, 0
PREV_WIDTH, PREV_HEIGHT, PREV_FLAGS, PREV_DEPTH, PREV_VSYNC = 0, 0, 0, 0, 0

INITIALIZED = False
FRAMEBUFFER = None
INSTANCE = None
WIDTH, HEIGHT = 0, 0
FLAGS = 0
DEPTH = 0
VSYNC = 0

# framebuffer scale and stuff
XSCALE, YSCALE = 1, 1


# static file
def create_instance(t, w, h, f=0, b=32, v=1, framebuffer=False):
    """Only one window instance is available at a time"""
    global INITIALIZED, WIDTH, HEIGHT, FLAGS, DEPTH, VSYNC, INSTANCE, ORIGINAL_HEIGHT, ORIGINAL_WIDTH, FRAMEBUFFER
    if not INITIALIZED:
        ORIGINAL_WIDTH, ORIGINAL_HEIGHT = w, h
        pygame.init()
        INITIALIZED = True
        INSTANCE = pygame.display.set_mode((w, h), flags=f, depth=b, vsync=v)
        FRAMEBUFFER = pygame.Surface((w, h)).convert()
    else:
        INSTANCE = pygame.display.set_mode((w, h), flags=f, depth=b, vsync=v)
    WIDTH, HEIGHT, FLAGS, DEPTH, VSYNC = w, h, f, b, v
    return INSTANCE


def get_instance():
    """returns the instance"""
    return INSTANCE


def get_framebuffer():
    """returns the framebuffer"""
    return FRAMEBUFFER


def handle_resize(resize_event):
    """Handle window resize event"""
    global PREV_WIDTH, PREV_HEIGHT, WIDTH, HEIGHT
    PREV_WIDTH, PREV_HEIGHT = WIDTH, HEIGHT
    WIDTH, HEIGHT = resize_event.x, resize_event.y


