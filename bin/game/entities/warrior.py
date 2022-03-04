import pygame
import random

from bin.maths import lerp
from bin.engine import entity
from bin.engine import animation


# open the warrior data file
warrior_animations = None
warrior_area = [32, 32]
warrior_lerp_amt = (30, 30)
warrior_hitbox_offsets = [0, 0]
warrior_offsets = [0, 0]
warrior_search_radius = 100

WARRIOR_ANIMATIONS = ["idle", "run", "attack", "death"]


def init():
    global warrior_animations
    warrior_animations = animation.AnimationData(jsonpath="assets/animations/warrior/warrior.json")


class Warrior(entity.Entity):
    def __init__(self, pos, frame=0):
        super().__init__(pos=pos, area=warrior_area, image_file=None)
        # animation handler!
        self.animation_access = animation.Animation(ani_data=warrior_animations,
                                                    current_animation=WARRIOR_ANIMATIONS[Warrior.STATIC],
                                                    frame=frame)
        # get image for the warrior
        self.image = self.animation_access.get_frame(warrior_animations)

        # set and lerp variables
        self.offsets = warrior_offsets
        self.hitbox_offsets = warrior_hitbox_offsets
        self.lerp_amt = warrior_lerp_amt

    def update(self, handler, world, dt):
        # update animation handler
        if self.sc:
            self.animation_access.set_animation(WARRIOR_ANIMATIONS[self.state], warrior_animations)
            self.sc = False
        self.update_animation_handler(self.animation_access, warrior_animations, dt)

        # don't move yet!
        # TODO - make movement script and entity AI
        # wander around for now
        # self.add_motion(50*dt, 50*dt)
        self.is_static()

        self.motion = [lerp(self.motion[0], 0.0, 0.3), lerp(self.motion[1], 0.0, 0.3)]
        world.move_entity(self)
        self.update_pos(world)

        # move the entity in the world!
        # TODO - add world movement and collision detection between objects and entity


