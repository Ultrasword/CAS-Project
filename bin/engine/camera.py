import pygame
from bin import maths
from bin.engine import event, handler, state


def render_text(window, font, text, pos, size=None, aa=True, color=(255, 255, 255), back=None):
    """Render text onto a window"""
    tf = font.render(text, aa, color, back)
    if size:
        tf = pygame.transform.scale(tf, (size[0] * len(text), size[1]))
    # render text
    window.blit(tf, pos)


class Camera:
    """Camera object for rendering and positioning while moving"""

    def __init__(self, window_size=[1280, 720], target=None):
        """Iniitalize a Camera Object"""
        # default chunk position
        self.chunkpos = [0, 0]
        # zoom -> to be inplemented later
        # TODO-implement zooming
        self.zoom = [1, 1]
        # default window area
        self.area = window_size
        # half area, no unecassary calculations
        self.half_area = [self.area[0] // 2, self.area[1] // 2]
        # center is just a more dynamic variable for the half area
        self.center = self.half_area.copy()
        # the target entity -> camera will follow this entity
        self.target_entity = target

    def update_position_with_target(self):
        """Render the world with the target entity at its center"""
        if self.target_entity:
            self.center = [self.half_area[0] - self.target_entity.pos[0] - self.target_entity.area[0] // 2,
                           self.half_area[1] - self.target_entity.pos[1] - self.target_entity.area[1] // 2]
            if self.chunkpos != self.target_entity.chunk:
                pygame.event.post(event.FOCAL_CHANGE_EVENT)
                self.chunkpos = self.target_entity.chunk

    def set_target(self, target):
        """Set a target entity for the camera to follow"""
        self.target_entity = target

    def set_position(self, position):
        """Set the position for the camera"""
        self.center = [self.half_area[0] - position[0],
                       self.half_area[1] - position[1]]
        # calculate pos and demonstrate chunk changes
        f = False
        pos = (-self.center[0] // handler.CHUNK_SIZE_PIX, -self.center[1] // handler.CHUNK_SIZE_PIX)
        if pos[0] != self.chunkpos[0]:
            self.chunkpos[0] = pos[0]
            f = True
        if pos[1] != self.chunkpos[1]:
            self.chunkpos[1] = pos[1]
            f = True
        if f:
            pygame.event.post(event.FOCAL_CHANGE_EVENT)

    def render_and_update_with_camera(self, window, dt):
        """Render and update the screen with a camera"""
        # render chunks first
        for p_string in state.WORLD.active_chunks:
            if chunk := state.WORLD.get_chunk(p_string, create=False):
                chunk.render(window, state.WORLD, self.center)
        for p_string in state.WORLD.active_chunks:
            if chunk := state.WORLD.get_chunk(p_string, create=False):
                chunk.render_blocks(window, state.WORLD, self.center)
        # next update the entities
        for ent in state.HANDLER.active_entities:
            e = state.HANDLER.entities[ent]
            e.update(state.HANDLER, state.WORLD, dt)
            if e.image:
                window.blit(e.image, [int(e.pos[0] + e.offsets[0] + self.center[0]),
                                      int(e.pos[1] + e.offsets[1] + self.center[1])])
        # particles
        state.PARTICLE.update_and_render_particles(window, dt)

    def debug_render(self, window):
        """Render the debug information -> hitboxes, chunk borders, etc"""
        # render the debug info as well
        for id, e in state.WORLD.entities.items():
            pygame.draw.lines(window, (255, 0, 0), True, (
                (e.pos[0] + self.center[0], e.pos[1] + self.center[1]),
                (e.pos[0] + self.center[0], e.pos[1] + e.area[1] + self.center[1]),
                (e.pos[0] + e.area[0] + self.center[0], e.pos[1] + e.area[1] + self.center[1]),
                (e.pos[0] + e.area[0] + self.center[0], e.pos[1] + self.center[1])
            ), width=2)
        # next you can render chunks

    def render_at(self, window, img, x=None, y=None, xoff=0, yoff=0):
        # calculate positiong
        pos = [0, 0]
        if x is not None:
            pos[0] = x + xoff
        else:
            pos[0] = self.center[0] + xoff
        if y is not None:
            pos[1] = y + yoff
        else:
            pos[1] = self.center[1] + yoff
        window.blit(img, pos)
