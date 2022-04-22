"""
Custom script class

- must init class before starting

"""
import pygame

from engine import handler, animation, state
from engine import user_input, maths, window
from engine import draw


PLAYER_ANIMATION_PATH = "assets/animations/tomato/tomato.json"
PLAYER_ENTITY_TYPE = "player_object"
PLAYER_ANIMATION_DATA = None
PLAYER_OBJECT_DATA = None

PLAYER_MAX_MOVEX = 3
PLAYER_MAX_MOVEY = 30

PLAYER_JUMP_SPEED = 30
PLAYER_MOVE_X = 70


def __init__():
    """
    Initialize the module
    
    - load animations, audio, other stuff
    """
    global PLAYER_ANIMATION_PATH, PLAYER_ANIMATION_DATA, PLAYER_ANIMATION_REGISTRY, PLAYER_OBJECT_DATA
    PLAYER_OBJECT_DATA = handler.ObjectData(100, 100, 100, 100)
    PLAYER_ANIMATION_DATA = animation.create_animation_handler_from_json(PLAYER_ANIMATION_PATH)

class Player(handler.PersistentObject):
    def __init__(self):
        """Player constructor"""
        super().__init__()
        
        self.object_type = PLAYER_ENTITY_TYPE

    def start(self):
        """Start method"""
        PLAYER_OBJECT_DATA.set_object_params(self)
        self.animation = PLAYER_ANIMATION_DATA.get_registry()
        self.image = self.ani_registry.get_frame()
        self.rect.area = self.ani_registry.frame_dim
    
    def update(self, dt: float) -> None:
        """Update function"""
        self.update_animation(dt)
        if user_input.is_key_pressed(pygame.K_a):
            self.m_motion[0] -= PLAYER_MOVE_X * dt
        if user_input.is_key_pressed(pygame.K_d):
            self.m_motion[0] += PLAYER_MOVE_X * dt
        if user_input.is_key_clicked(pygame.K_SPACE):
            self.m_motion[1] -= PLAYER_JUMP_SPEED
        
        # add gravity
        self.m_motion[1] += state.CURRENT.gravity * dt
        state.CURRENT.move_object(self)
        
        # lerp
        # print(self.m_moving)
        if not self.m_moving[0]:
            self.m_motion[0] = maths.clamp(maths.lerp(self.m_motion[0], 0.0, 0.5), -PLAYER_MAX_MOVEX, PLAYER_MAX_MOVEX)
        if not self.m_moving[1]:
            self.m_motion[1] = maths.clamp(maths.lerp(self.m_motion[1], 0.0, 0.3), -PLAYER_MAX_MOVEY, PLAYER_MAX_MOVEY)

    def render(self):
        """Render function"""
        window.draw_buffer(self.image, self.rect.pos)
        draw.DEBUG_DRAW_LINES(window.get_framebuffer(), (255, 0, 0), True, (self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft))


# register player type
handler.register_object_type(PLAYER_ENTITY_TYPE, Player)
