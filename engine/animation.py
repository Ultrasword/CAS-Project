from . import filehandler


class AnimationData:
    def __init__(self, images, size, frame_time, base_folder=""):
        """Constructor for animation data storing object"""
        self.frames = []
        self.f_count = len(images)-1
        self.size = size
        # load images with pygame
        for img in images:
            self.frames.append(filehandler.scale(filehandler.get_image_without_cache(base_folder + img), size))
        # then save frame times
        self.frame_time = frame_time


class AnimationRegistry:
    def __init__(self, aid):
        """Constructor for Animation Registry object - a reference should be made in the parent entity"""
        self.aid = aid
        self.frame = 0
        self.frame_time = 0


class AnimationHandler:
    def __init__(self, ani_data: AnimationData):
        """Animation handler - handles different entities who want to access the same animation"""
        self.aid_gen = 0
        self.ani_data = ani_data
        self.registries = {}
    
    def update_registry(self, aid, dt):
        """Update an animation registry - animation registries are linked to the entity it is in"""
        self.registries[aid].frame_time += dt
        if self.registries[aid].frame_time > self.ani_data.frame_time[self.registries[aid].frame]:
            self.registries[aid].frame_time = 0
            self.registries[aid].frame += 1
            if self.registries[aid].frame > self.ani_data.f_count:
                self.registries[aid].frame = 0
            return True

    def get_frame(self, aid):
        """Get a specific frame for a specific entity"""
        return self.ani_data.frames[self.registries[aid].frame]

    def register_entity(self, entity):
        """Register an entity to this animation handler"""
        entity.aid = self.gen_aid()
        self.registries[entity.aid] = AnimationRegistry(entity.aid)

    def gen_aid(self):
        """Returns a unique ID for this animation handler"""
        self.aid_gen += 1
        return self.aid_gen

