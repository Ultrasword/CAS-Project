import pygame

import engine
from engine import window, clock, user_input, filehandler, handler, chunk, statehandler, state, entity, tile
from game.entities import player


# for import tests
# exit()

# create a window
window.create_instance("CAS Project", 1280, 720, 0, 32, 0)
tile.init_tiles("assets/tiles")

background = (255, 255, 255)


# ------------- TESTS ----------------------
player.load_player_module()
p = player.Player(600, 100)

s = state.State()
# e = entity.Entity()
# entity.set_entity_properties(100, 100, 100, 100, "assets/unknown.png", e)
# s.handler.add_entity(e)
s.handler.add_entity(p)

# s.handler.add_entity(player.Player(200, 200))


c = chunk.Chunk(0, 0)
# for x in range(chunk.CHUNK_WIDTH):
#     for y in range(chunk.CHUNK_HEIGHT):
#         t = chunk.create_tile(x, y, "assets/grass.png")
#         c.set_tile_at(t)
s.handler.add_chunk(c)

for y in range(chunk.CHUNK_HEIGHT):
    c.set_tile_at(chunk.create_tile(5, y, "grass", 1))
    c.set_tile_at(chunk.create_tile(1, y, "code", 0))


# must set chunk to active bc it has not been automated yet
s.handler.active_chunks.append(c.id)

statehandler.push_state(s)

# ------------------------------------------


clock.start(fps=30)
window.create_clock(clock.FPS)
running = True
while running:
    # updates
    window.FRAMEBUFFER.fill(background)
    
    # render world and update stuff
    statehandler.CURRENT.handler.render_chunks(window.FRAMEBUFFER, (0,0))       # TODO - add camera thing
    statehandler.CURRENT.handler.update_and_render_entities(window.FRAMEBUFFER, clock.delta_time, (0,0)) # TODO - same here

    # render
    # window.INSTANCE.blit(pygame.transform.scale(window.FRAMEBUFFER, (window.WIDTH, window.HEIGHT)), (0,0))
    window.INSTANCE.blit(window.FRAMEBUFFER, (0,0))
    pygame.display.flip()

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
    # update keyboard
    user_input.update()

    # print(user_input.get_mouse_pos())

    # update clock
    clock.update()
    window.GLOBAL_CLOCK.tick(clock.FPS)

pygame.quit()