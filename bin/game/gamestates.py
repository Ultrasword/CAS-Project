import numpy as np
import pygame

from bin import maths
from bin.engine import state
from bin.engine import handler


# constants
CAMERA_MOVE_SPEED = 500
CAMERA_MOTION = [0, 0]
CAMERA_POSITION = [0, 0]
CAMERA_LERP = 0.5


class InGame(state.GameState):
    def __init__(self, mp, camera_pos=[0,0], entities=None, chunks=None, seed=None):
        super(InGame, self).__init__(mp, entities, chunks, seed)
        global CAMERA_POSITION
        CAMERA_POSITION = camera_pos
        self.cam_border = [0, 0,
                           handler.CHUNK_SIZE_PIX*handler.WORLD_CHUNK_WIDTH,
                           handler.CHUNK_SIZE_PIX*handler.WORLD_CHUNK_HEIGHT]

    def update_cam(self, dt, camera):
        CAMERA_MOTION[0] = maths.lerp(CAMERA_MOTION[0], 0.0, CAMERA_LERP)
        CAMERA_MOTION[1] = maths.lerp(CAMERA_MOTION[1], 0.0, CAMERA_LERP)
        if state.USER.keyboard.is_pressed(pygame.K_LEFT):
            CAMERA_MOTION[0] -= CAMERA_MOVE_SPEED * dt
        if state.USER.keyboard.is_pressed(pygame.K_RIGHT):
            CAMERA_MOTION[0] += CAMERA_MOVE_SPEED * dt
        if state.USER.keyboard.is_pressed(pygame.K_DOWN):
            CAMERA_MOTION[1] += CAMERA_MOVE_SPEED * dt
        if state.USER.keyboard.is_pressed(pygame.K_UP):
            CAMERA_MOTION[1] -= CAMERA_MOVE_SPEED * dt
        CAMERA_POSITION[0] += CAMERA_MOTION[0]
        CAMERA_POSITION[1] += CAMERA_MOTION[1]
        if CAMERA_POSITION[0] - camera.half_area[0] < self.cam_border[0]:
            CAMERA_POSITION[0] = camera.half_area[0]
        elif CAMERA_POSITION[0] + camera.half_area[0] > self.cam_border[2]:
            CAMERA_POSITION[0] = self.cam_border[2] - camera.half_area[0]
        if CAMERA_POSITION[1] - camera.half_area[1] < self.cam_border[1]:
            CAMERA_POSITION[1] = camera.half_area[1]
        elif CAMERA_POSITION[1] + camera.half_area[1] > self.cam_border[3]:
            CAMERA_POSITION[1] = self.cam_border[3] - camera.half_area[1]
        camera.set_position([int(CAMERA_POSITION[0]), int(CAMERA_POSITION[1])])
