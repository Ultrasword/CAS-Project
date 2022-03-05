import pygame

from engine import window, clock


# create a window
window.create_instance("CAS Project", 1280, 720, 0, 32, 1)


clock.start(fps=30)
running = True
while running:
    # updates

    # render
    pygame.display.flip()

    for e in pygame.event.get():
        # handle different events
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            # keyboard press
            pass
        elif e.type == pygame.KEYUP:
            # keyboard release
            pass
        elif e.type == pygame.MOUSEMOTION:
            # mouse movement
            pass
        elif e.type == pygame.MOUSEBUTTONDOWN:
            # mouse press
            pass
        elif e.type == pygame.MOUSEBUTTONUP:
            # mouse release
            pass
        elif e.type == pygame.WINDOWRESIZED:
            # window resized
            window.handle_resize(e)
    clock.update()
