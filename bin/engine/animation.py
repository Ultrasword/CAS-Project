import pygame
import json
from bin.engine import filehandler


class AnimationData:
    def __init__(self, jsonpath=None, flags=0):
        # class data
        self.animations = {}
        self.width = 0
        self.height = 0
        self.xoffset = 0
        self.yoffset = 0

        if jsonpath:
            with open(jsonpath, 'r') as file:
                data = json.load(file)
                file.close()
            # get image width and height
            self.width = data["width"]
            self.height = data["height"]
            self.xoffset = data["xoffset"]
            self.yoffset = data["yoffset"]
            # use data to get all animation data!
            for ani in data["animations"]:
                # load the animation
                p = data[ani]["path"]
                frame_time = 1 / data[ani]["fps"]
                frames = data[ani]["frames"]
                ani_frames = filehandler.load_animation_from_sprite_sheet(p, self.width, self.height, frames,
                                                                          self.xoffset, self.yoffset)
                self.animations[ani] = [
                    p,  # the path to the sprite sheet
                    frame_time,  # the time between frames
                    ani_frames,  # frame data -> holds the animation frames
                    frames
                ]
        # print(self.animations)


class Animation:
    def __init__(self, ani_data=None, current_animation=None, frame=0, clock=0):
        # time management and frame handling
        self.clock = clock
        self.current_animation = current_animation
        self.frame = frame
        self.current_frame_time = 0
        self.frame_changed = False
        self.current_frame_cap = 0

        if current_animation:
            self.set_animation(current_animation, ani_data, frame)

    def set_animation(self, ani, ani_data, frame=0):
        self.current_animation = ani
        self.current_frame_time = ani_data.animations[ani][1]
        self.frame = frame
        self.frame_changed = True
        self.current_frame_cap = ani_data.animations[ani][3]

    def set_frame(self, frame):
        self.frame = frame

    def get_frame(self, ani_data, xflip=False, yflip=False):
        if xflip or yflip:
            return pygame.transform.flip(ani_data.animations[self.current_animation][3][self.frame], xflip, yflip)
        return ani_data.animations[self.current_animation][2][self.frame]

    def update(self, dt):
        # check if it has an animation
        if not self.current_animation:
            return
        # otherwise continue
        self.clock += dt
        while self.clock >= self.current_frame_time:
            # if time limit passed for the frame, increase frame
            self.frame += 1
            if self.frame >= self.current_frame_cap:
                self.frame = 0
            self.frame_changed = True
            self.clock -= self.current_frame_time
