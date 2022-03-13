import json
import pygame

from engine import animation, filehandler, entity, user_input


PLAYER_ANIMATION_PATH = "assets/animations/player/"
INFO_FILE = "info.json"

# player width and stuff
PLAYER_WIDTH = 0
PLAYER_HEIGHT = 0

# constants related to player
PLAYER_IDLE = "idle"
PLAYER_WALK = "walk"
PLAYER_RUN = "run"
PLAYER_ATTACK = "attack"

MAX_HEALTH = 200
WALK_SPEED = 50
RUN_SPEED = 80
WEIGHT = 100 # we use this to calculate friction :D


player_animations = None


def load_player_module():
    """Loads player module"""
    global player_animations
    player_animations = {}
    # load json file
    with open(PLAYER_ANIMATION_PATH + INFO_FILE) as file:
        data = json.load(file)
        file.close()
    # get data
    player_size = data["player size"]
    image_path = data["image path"]
    for name, anidata in data["animations"].items():
        w, h = anidata["width"], anidata["height"]
        # create the animation block
        data_block = animation.AnimationData(anidata["images"], (w,h), anidata["time"])
        # now store it in the cache
        player_animations[name] = animation.AnimationHandler(data_block)


class Player(entity.Entity):
    def __init__(self, x, y):
        """Player object constructor"""
        super().__init__()
        # set parameters
        entity.set_entity_properties(x, y, PLAYER_WIDTH, PLAYER_HEIGHT, None, self)

        # set animation stuff
        for ani in player_animations:
            player_animations[ani].register_entity(self)
        # set idle state
        self.set_state(PLAYER_IDLE)
        self.image = player_animations[self.state].get_frame(self.aid)

        # gameplay
        # TODO - make health bar object
        self.health = 0
    
    def update(self, dt):
        if user_input.is_key_pressed(pygame.K_d):
            self.motion[0] += 100 * dt
        if user_input.is_key_pressed(pygame.K_a):
            self.motion[0] -= 100 * dt
        
        # yes
        self.update_position()

