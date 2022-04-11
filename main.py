import pygame

import engine
from engine import window, clock, user_input, handler, draw, filehandler, maths



background = (255, 255, 255)

# create essential instances
window.create_instance("Template", 1280, 720, f=pygame.RESIZABLE)
window.set_scaling(True)
window.change_framebuffer(1280, 720, pygame.SRCALPHA)



# handler object -> # TODO - abstract later 
HANDLER = handler.Handler()



# -------- testing ------ #

img = filehandler.get_image("test/images/test1.png")

object_data = handler.ObjectData(100, 100, 100, 100)

class test(handler.Object):
    def __init__(self):
        super().__init__()
        # set params
        object_data.set_object_params(self)
        # image
        self.image = filehandler.scale(img, self.area)
    
    def update(self, dt):
        # print(dt)
        if user_input.is_key_pressed(pygame.K_a):
            self.motion[0] -= 100 * dt
        if user_input.is_key_pressed(pygame.K_d):
            self.motion[0] += 100 * dt
        if user_input.is_key_pressed(pygame.K_w):
            self.motion[1] -= 100 * dt
        if user_input.is_key_pressed(pygame.K_s):
            self.motion[1] += 100 * dt
        
        # lerp
        self.motion[0] = maths.lerp(self.motion[0], 0.0, 0.3)
        self.motion[1] = maths.lerp(self.motion[1], 0.0, 0.3)

        self.pos[0] += self.motion[0]
        self.pos[1] += self.motion[1]

    def render(self):
        window.draw_buffer(self.image, self.pos)
        # draw some lines facing the direction of the motion
        c = self.center
        draw.DEBUG_DRAW_LINE(window.get_framebuffer(), (255,0,0), c, (c[0] + self.motion[0] * 10, c[1] + self.motion[1] * 10), 1)

HANDLER.add_entity_auto(test())

# ----------------------- #


clock.start(fps=30)
window.create_clock(clock.FPS)
running = True
while running:
    # fill instance
    window.fill_buffer(background)

    # updates
    HANDLER.handle_entities(clock.delta_time)

    # render
    window.push_buffer((0,0))
    pygame.display.flip()

    # update keyboard and mouse
    user_input.update()
    # for loop through events
    for e in pygame.event.get():
        # handle different events
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            # keyboard press
            user_input.key_press(e)
        elif e.type == pygame.KEYUP:
            # keyboard release
            user_input.key_release(e)
        elif e.type == pygame.MOUSEMOTION:
            # mouse movement
            user_input.mouse_move_update(e)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            # mouse press
            user_input.mouse_button_press(e)
        elif e.type == pygame.MOUSEBUTTONUP:
            # mouse release
            user_input.mouse_button_release(e)
        elif e.type == pygame.WINDOWRESIZED:
            # window resized
            window.handle_resize(e)
            user_input.update_ratio(window.WIDTH, window.HEIGHT, window.ORIGINAL_WIDTH, window.ORIGINAL_HEIGHT)
        elif e.type == pygame.WINDOWMAXIMIZED:
            # window maximized
            window.get_instance().fill(background)
            # re render all entities
            HANDLER.render_all()
            # push frame
            pygame.display.update()
            # prevent re push
            window.INSTANCE_CHANGED = False

    # update clock -- calculate delta time
    clock.update()
    # update global clock - time sleep for vsync
    window.GLOBAL_CLOCK.tick(clock.FPS)

pygame.quit()
