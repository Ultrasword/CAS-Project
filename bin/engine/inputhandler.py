import pygame


def change_mapped_key(key_num, value):
    InputHandler.default_key_map[key_num] = value


class InputHandler:
    default_key_map = {
        pygame.K_w: 'up',
        pygame.K_s: 'down',
        pygame.K_d: 'right',
        pygame.K_a: 'left',
        pygame.K_SPACE: 'jump',
        pygame.K_LSHIFT: 'shift',
        pygame.K_ESCAPE: 'esc'
    }

    def __init__(self):
        self.keymap = InputHandler.default_key_map
        self.key_pressed = {x: False for x in InputHandler.default_key_map.values()}

    def pressed(self, key):
        return self.key_pressed.get(key)

    def update(self, pygame_event):
        if pygame_event.type == pygame.KEYDOWN:
            self.key_pressed[pygame_event.key] = True
        elif pygame_event.type == pygame.KEYUP:
            self.key_pressed[pygame_event.key] = False