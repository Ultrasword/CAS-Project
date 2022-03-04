import pygame


class Window:
    FULLSCREEN_SIZE = None

    def __init__(self, width, height, title=None, flags=0, bit_depth=32, icon=None, vsync=0):
        pygame.init()
        # some globals
        self.FULLSCREEN_SIZE = pygame.display.get_desktop_sizes()[0]
        self.previous_window_settings = [(width, height), flags, bit_depth, vsync]

        self.base_area = (width, height)
        self.area = [width, height]
        self.title = title
        self.icon = icon
        self.flags = flags
        self.bit_depth = bit_depth
        self.vsync = vsync

        # create the window
        self.window = pygame.display.set_mode(self.area, self.flags, self.bit_depth, vsync=self.vsync)
        self.sdlwindow = None
        self.size_changed = True
        self.min_size = None
        self.fullscreen = False
        self.windowed_fullscreen = False
        self.w_f_toggle = 0

        if self.title:
            pygame.display.set_caption(self.title)
        if self.icon:
            pygame.display.set_icon(pygame.image.load(self.icon))

    def set_min_size(self, w, h):
        self.min_size = (w, h)

    def get_window(self):
        return self.window

    def change_dimension(self, width, height):
        self.area = [width, height]
        # if self.area[0] < self.min_size[0]:
        #     self.area[0] = self.min_size[0]
        # if self.area[1] < self.min_size[1]:
        #     self.area[1] = self.min_size[1]
        # self.window = pygame.display.set_mode(self.area, self.flags, self.bit_depth)
        self.size_changed = True

    def toggle_windowed_fullscreen(self):
        # dont change window size / type
        self.w_f_toggle += 1
        if self.w_f_toggle == 1:
            self.windowed_fullscreen = not self.windowed_fullscreen
            self.w_f_toggle = 0
            self.size_changed = True
            if self.windowed_fullscreen:
                self.previous_window_settings = [self.area, self.flags,
                                                 self.bit_depth, self.sdlwindow.position]
                self.area = self.FULLSCREEN_SIZE
                self.window = pygame.display.set_mode(self.FULLSCREEN_SIZE, pygame.NOFRAME, 32)
                self.sdlwindow.position = (0, 0)
            else:
                self.window = pygame.display.set_mode(self.previous_window_settings[0],
                                                      self.previous_window_settings[1],
                                                      self.previous_window_settings[2])
                self.area = self.previous_window_settings[0]
                self.sdlwindow.position = self.previous_window_settings[3]
