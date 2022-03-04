# main file!
import os
import json
import pygame
import random
import traceback

from pygame._sdl2.video import Window as sdlWindow

from bin.engine import window, clock, event, state, ui, camera

from bin import game

os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    # create all necessary objects
    window_scale_size = (1280, 720)
    window_blit_location = (0, 0)
    RENDER_DISTANCE = 2
    BACKGROUND_COLOR = (255, 255, 255)

    Window = window.Window(1280, 720, "WageWar.io", pygame.BLEND_RGBA_MAX | pygame.RESIZABLE, bit_depth=32, vsync=1)
    Window.sdlwindow = sdlWindow.from_display_module()
    Window.set_min_size(1280, 720)
    Clock = clock.Clock(60)
    frame_buffer = pygame.Surface(window_scale_size, pygame.SRCALPHA, 32).convert()
    running = True


    # create a camera
    CAMERA = camera.Camera(window_scale_size)

    # make a state
    state.init(CAMERA, None)
    state.USER = ui.User()
    state.push_state(state.GameState(None))
    # state.CURRENT_STATE.add_entity()


    # run processes
    Clock.start()
    count = 1
    # game loop
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
            # window resize
            elif e.type == pygame.WINDOWRESIZED:
                Window.change_dimension(e.x, e.y)
                state.USER.mouse.update_ratio(e.x, e.y, window_scale_size[0], window_scale_size[1])
            # keyboard - keydown
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_F11:
                    Window.toggle_windowed_fullscreen()
                else:
                    state.USER.keyboard.press_key(e.key)
            # keyboard - keyup
            elif e.type == pygame.KEYUP:
                state.USER.keyboard.release_key(e.key)
            # handle mouse movement
            elif e.type == pygame.MOUSEMOTION:
                state.USER.mouse.mouse_move_update(e)
            # handle mouse press
            elif e.type == pygame.MOUSEBUTTONDOWN:
                state.USER.mouse.mouse_press(e)
            elif e.type == pygame.MOUSEBUTTONUP:
                state.USER.mouse.mouse_release(e)
            # special event
            elif e.type == event.FOCAL_CHANGE_EVENT_ID:
                state.WORLD.calculate_relavent_chunks(state.CAMERA.chunkpos, RENDER_DISTANCE, l_bor=0, t_bor=0)
            elif e.type == event.USER_DRAG_RELEASE_ID:
                event.user_drag_event(e, state.WORLD, state.HANDLER)
            else:
                # do later
                pass
        
        # render stuff and update everything
        frame_buffer.fill(BACKGROUND_COLOR)
        # render with camera
        if state.CURRENT_STATE:
                # get camera moving
            state.CURRENT_STATE.update_cam(Clock.delta_time, state.CAMERA)

            state.CURRENT_STATE.update_systems(Clock.delta_time)
            state.CAMERA.render_and_update_with_camera(frame_buffer, Clock.delta_time)
            state.CURRENT_STATE.render_systems(frame_buffer)

        # render the frame_buffer onto the screen
        Window.window.blit(pygame.transform.scale(frame_buffer, Window.area), window_blit_location)

        pygame.display.flip()
        Clock.update()
        Clock.wait()

if __name__ == "__main__":
    main()
