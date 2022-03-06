import pygame

from engine import window, clock, user_input, filehandler, handler, chunk, statehandler, state, entity

# create a window
window.create_instance("CAS Project", 1280, 720, 0, 32, 0)

background = (255, 255, 255)


# ------------- TESTS ----------------------
s = state.State()
e = entity.Entity()
entity.set_entity_properties(100, 100, 100, 100, "assets/unknown.png", e)
s.handler.add_entity(e)

statehandler.push_state(s)


# ------------------------------------------



clock.start(fps=30)
running = True
while running:
    # updates
    window.FRAMEBUFFER.fill(background)
    statehandler.CURRENT.handler.update_and_render_entities(window.FRAMEBUFFER, clock.delta_time)
    statehandler.CURRENT.handler.render_chunks(window.FRAMEBUFFER)

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

pygame.quit()