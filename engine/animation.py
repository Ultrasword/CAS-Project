import os
import json
from engine import filehandler


ANIMATION_NAME = "name"
ANIMATION_IMAGES = "images"
ANIMATION_FRAME_TIMES = "times"
ANIMATION_FRAME_SIZE = "sizes"


animation_handler_cache = {}


def cache_animations(animation_data: dict):
    """Create Animation Handler object and cache everything"""
    global animation_handler_cache

    name = animation_data[ANIMATION_NAME]
    images = animation_data[ANIMATION_IMAGES]
    sizes = animation_data[ANIMATION_FRAME_SIZE]
    frame_time = animation_data[ANIMATION_FRAME_TIMES]

    animation_handler_cache[name] = AnimationHandler(name, images, sizes, frame_time)


# ------------- Animation Registry --------------- //
REGISTRY_COUNT_ID = 0

def GET_REGISTRY():
    global REGISTRY_COUNT_ID
    REGISTRY_COUNT_ID += 1
    return REGISTRY_COUNT_ID


class AnimationRegistry:
    def __init__(self, handler):
        """Animation Registry constructor"""
        self.register_id = 0
        self.frame = 0
        self.time_passed = 0
        self.changed = True
        self.frame_dim = handler.image_sizes[self.frame]

        # animatino handler
        self.handler = handler
    
    def update(self, dt):
        """Update Animation Registry"""
        self.time_passed += dt
        if self.time_passed > self.handler.frame_time:
            self.time_passed -= self.handler.frame_time
            self.frame += 1
            self.changed = True
            if self.frame >= self.handler.frame_count:
                self.frame = 0
        
    def get_frame(self):
        """Get the current frame"""
        return self.handler.images[self.frame]


# -------------- image loading functions ------------- #

def iterate_load_image_list(base: str, images: list, ext:str=None):
    """Load images and yield them"""
    for img in images:
        if ext:
            img += ext
        print(os.path.join(base, img))
        yield filehandler.get_image(os.path.join(base, img))


def load_image_list(base: str, images: list, ext:str=None)-> list:
    """Load images from a list of strings"""
    return list(iterate_load_image_list(base, images, ext=ext))


class AnimationHandler:
    def __init__(self, name: str, images: list, image_sizes: list, fps: int):
        """Animation Handler constructor"""
        self.name = name
        self.images = images
        self.image_sizes = image_sizes
        self.frame_time = 1/fps
        self.frame_count = len(images)

    def get_registry(self):
        """Register a registry to this animation handler"""
        return AnimationRegistry(self)


def create_animation_handler_from_json(json_path: str) -> AnimationHandler:
    """Create an animatino handler object from json file"""
    with open(json_path, 'r') as file:
        data = json.load(file)
        file.close()
    name = data["name"]
    base_path = data["base_path"]
    image_paths = data["images"]
    fps = data["fps"]
    ext = data.get("ext")
    sizes = data.get("sizes")
    size = data.get("size")
    
    dif_sizes = sizes != None

    # load images
    result_images = []
    for i, result in enumerate(iterate_load_image_list(base_path, image_paths, ext=ext)):
        if dif_sizes:
            # you should index to the right size
            result_images.append(filehandler.scale(result, sizes[i]))
        else:
            # just stick
            result_images.append(filehandler.scale(result, size))
    
    # create animation handler
    return AnimationHandler(name, result_images, sizes if dif_sizes else [size for i in range(len(image_paths))], fps)
