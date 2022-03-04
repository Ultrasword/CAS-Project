from . import filehandler


# update functions
def static_update(handler, pid, particle, dt):
    # update the position and time
    particle[6] += dt
    if particle[6] > particle[5]:
        # remove particle
        handler.remove_next.append(pid)
    particle[0] += particle[2] * dt
    particle[1] += particle[3] * dt


def ani_update(handler, pid, particle, dt):
    # update position and time
    particle[6] += dt
    if particle[6] > particle[5]:
        # remove particle
        handler.remove_next.append(pid)
    particle[0] += particle[2] * dt
    particle[1] += particle[3] * dt
    # update animation
    particle[10] += dt
    if particle[10] > particle[11]:
        particle[10] = 0
        # increase frame
        particle[12] += 1
        if particle[12] >= handler.BUFFER[particle[9][0]][particle[9][1]][0]:
            particle[12] = 0


def static_render(handler, window, particle):
    window.blit(handler.BUFFER[particle[9][0]][particle[9][1]], [int(particle[0]), int(particle[1])])


def animated_render(handler, window, particle):
    window.blit(handler.BUFFER[particle[9][0]][particle[9][1]][1][particle[12]], [int(particle[0]), int(particle[1])])


class ParticleHandler:
    """
    Particles are designed as follows

                  0     1     2      3       4      5        6        7        8       9              10        11     12
    particle = [xpos, ypos, xmove, ymove, size, life, c_life, has_cfunc, func_id, (bit_id, img_id), fp_time, f_time, frame]
                                                          # index 10, 11, 12 excluded
                                                          when using non animated
                                                          particles

    if particle has custom func, then this is the layout

    Particle image and animation handling

    Images and animations are designed as follows

    TODO - add different sizes for particles
    TODO - allow img names to be changed when loading
    buffer = {
        bytesize :{
                img_path     1
            "normal image": img,
                            1    2
            "animation": size, images       # animations better all be same size
        }
    }

    """

    PARTICLE_CAP = 256
    PARTICLE_ID = 0

    # func id
    STATIC_IMG = 0
    ANIMATED_IMG = 1

    FUNC_COUNT = 2
    FUNCTIONS = [
        static_update,      # static
        ani_update          # ani
    ]

    RFUNC_COUNT = 2
    RENDER_FUNCTIONS = [
        static_render,      # static
        animated_render     # ani
    ]

    # image buffer
    BUFFER = {}

    def __init__(self):
        """Initialize a base Particle Handler object"""

        # stores particles based off id
        self.particles = {}
        self.remove_next = []

    def reset(self):
        self.particles.clear()
        self.remove_next.clear()

    def w_and_h_to_num(self, w, h):
        return (w << 8) + h

    def num_to_w_and_h(self, num):
        return [(w:=(num>>8)), num-(w<<8)]

    def load_image(self, path, size=None):
        """Load an image into buffer and return it"""
        image = filehandler.get_image(path, size=size)
        # get the bytesize
        if not size:
            size = image.get_size()
            bytesize = self.w_and_h_to_num(size[0], size[1])
        else:
            bytesize = self.w_and_h_to_num(size[0], size[1])

        # check if bytesize already exists
        if not self.BUFFER.get(bytesize):
            self.BUFFER[bytesize] = {}

        # add image to the bytesize
        self.BUFFER[bytesize][path] = image

        # return data
        return bytesize

    def load_animation(self, files, size=None):
        ani = [filehandler.get_image(file, size=size) for file in files[1:]]
        bytesize = self.w_and_h_to_num(ani[1].get_size()[0], ani[1].get_size()[1])
        if not self.BUFFER.get(bytesize):
            self.BUFFER[bytesize] = {}
        self.BUFFER[bytesize][files[0]] = (len(ani), ani)
        return bytesize

    def add_custom_func(self, func):
        self.FUNCTIONS[self.FUNC_COUNT] = func
        self.FUNC_COUNT += 1
        return self.FUNC_COUNT

    def remove_particle(self, id):
        self.particles.pop(id)

    def add_particle(self, x, y, mx, my, life, img_path, size=None, frame_time=None, custom_func=None):  # index 0 of img_path will be ani name
        """Creates a new Particle and adds it to the buffer"""
        # check if can add more particles
        if self.PARTICLE_ID >= self.PARTICLE_CAP:
            # TODO - remove the least relevant particle
            # remove particle that has been alive the longest
            self.particles.pop((self.PARTICLE_ID + 1) % self.PARTICLE_CAP)

        # create base
        pt = [x, y, mx, my, 0, life, 0, True if custom_func else False]
        # check if animation or static img
        if type(img_path) == list:
            # if is animation, check if all images are loaded
            bytesize = self.load_animation(img_path, size=size)      # load animation
            if custom_func:
                pt.append(self.add_custom_func(custom_func))    # add the func id to pt
            else:
                pt.append(self.ANIMATED_IMG)                    # state it is ani
            pt[4] = self.num_to_w_and_h(bytesize)
            pt.append((bytesize, img_path[0]))              # to reference ani from buffer
            pt.append(0)                        # timer variable for frame passed time
            pt.append(frame_time)               # add frame time
            pt.append(0)                        # for the frame
        else:
            # its a static image
            bytesize = self.load_image(img_path, size=size)           # load image
            if custom_func:
                pt.append(self.add_custom_func(custom_func))        # add the func id to pt
            else:
                pt.append(self.STATIC_IMG)                          # state it is static
            pt[4] = self.num_to_w_and_h(bytesize)
            pt.append((bytesize, img_path))                 # to reference img from buffer

        # TODO - maybe switch to using integer id's for loaded images | keep track of all images loaded and
        #  just give them an id

        # add particle
        self.particles[self.PARTICLE_ID] = pt
        self.PARTICLE_ID = (self.PARTICLE_ID + 1) % self.PARTICLE_CAP

    def update_and_render_particles(self, window, dt):
        """Updates and renders all particles"""
        for id, ent in self.particles.items():
            # move the particle
            self.FUNCTIONS[ent[8]](self, id, ent, dt)
            # render particles
            self.RENDER_FUNCTIONS[ent[8]](self, window, ent)
        for n in self.remove_next:
            self.remove_particle(n)
        self.remove_next.clear()

    def update_particles(self, dt):
        """Updates all particles"""
        for id, ent in self.particles.items():
            # move particle
            self.FUNCTIONS[ent[8]](self, id, ent, dt)
        for n in self.remove_next:
            self.remove_particle(n)
        self.remove_next.clear()

    def render_particles(self, window):
        """Render Particles"""
        for ent in self.particles.values():
            # render particle
            self.RENDER_FUNCTIONS[ent[8]](self, window, ent)
            