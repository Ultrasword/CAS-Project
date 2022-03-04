import pygame


def user_event_id():
    pygame.USEREVENT += 1
    return pygame.USEREVENT


# ENUMS
FOCAL_CHANGE_EVENT_ID = user_event_id()
USER_DRAG_RELEASE_ID = user_event_id()

# events
FOCAL_CHANGE_EVENT = pygame.event.Event(FOCAL_CHANGE_EVENT_ID)

# special storage
USER_SELECTED_ENTITIES = set()


def user_drag_event(event, world, handler):
    USER_SELECTED_ENTITIES.clear()
    # get selected area
    area = event.s + event.e
    # get all collided chunks
    chunks = world.get_collided_chunks_hitbox(area)
    for cs in chunks:
        for ent in world.get_chunk(cs, auto_start=False).entities:
            e = handler.entities[ent]
            if world.is_collided(area, e.pos+e.area):
                USER_SELECTED_ENTITIES.add(ent)
    # add all these items to the selected thing
    # print(USER_SELECTED_ENTITIES)
