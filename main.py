import pygame

import engine
from engine import window, clock, user_input, handler, draw
from engine import filehandler, maths, animation, state, serialize
from engine import spritesheet
from engine.globals import *

from scripts import player


background = (255, 255, 255)

# create essential instances
window.create_instance("Template", 1280, 720, f=pygame.RESIZABLE)
window.set_scaling(True)
window.change_framebuffer(1280, 720, pygame.SRCALPHA)

# init stuff
player.__init__()

# handler object -> # TODO - abstract later 
HANDLER = state.State.deserialize(serialize.load_json_data("test.json"))
state.push_state(HANDLER)


# -------- testing ------ #

c = HANDLER.make_template_chunk(1, 0)
for x in range(CHUNK_WIDTH):
    c.set_tile_at(c.create_grid_tile(x, 6, "assets/terrain/dirt.png", collide=True))

# ------------ Game Loop ----------- #

clock.start(fps=60)
window.create_clock(clock.FPS)
running = True
while running:
    # fill instance
    window.fill_buffer(background)

    # if reload 
    if user_input.is_key_clicked(114): # ctrl + r
        # reload
        print("reload")
        state.pop_state()
        state.push_state(state.State.deserialize(serialize.load_json_data("test.json")))

    # updates
    state.CURRENT.update(clock.delta_time)

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
