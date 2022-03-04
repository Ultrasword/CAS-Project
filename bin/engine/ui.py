import pygame
from bin.engine import window


MOUSEBUTTON_LEFT = 1
MOUSEBUTTON_MIDDLE = 2
MOUSEBUTTON_RIGHT = 3


class Mouse(object):
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.scroll_x = 0
        self.scroll_y = 0
        self.pressed = [False for i in range(4)]
        self.x_move = 0
        self.y_move = 0
        # for scaling mouse input
        self.x_ratio = 1
        self.y_ratio = 1

    def mouse_press(self, event):
        if event.button < 4:
            self.pressed[event.button] = True

    def mouse_release(self, event):
        if event.button < 4:
            self.pressed[event.button] = False

    def mouse_scroll_update(self, event):
        print(event)

    def mouse_move_update(self, event):
        self.x_move, self.y_move = event.rel[0], event.rel[1]
        self.x_pos, self.y_pos = event.pos[0], event.pos[1]

    def get_pos(self):
        return self.x_pos * self.x_ratio, self.y_pos * self.y_ratio

    def update_ratio(self, w, h, o_w, o_h):
        self.x_ratio = o_w / w
        self.y_ratio = o_h / h


class Keyboard(object):
    def __init__(self):
        self.keys = {}

    def is_pressed(self, key):
        if self.keys.get(key) is None:
            self.keys[key] = False
        return self.keys[key]

    def press_key(self, key):
        self.keys[key] = True

    def release_key(self, key):
        self.keys[key] = False


class User(object):
    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()
