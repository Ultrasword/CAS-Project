import time


class Clock:
    def __init__(self, fps=60):
        self.start_time = 0
        self.end_time = 0
        self.delta_time = 0
        self.wait_time = 0
        self.fps = fps
        self.ideal_time = 1 / self.fps

    def start(self):
        self.start_time = time.time()

    def update(self):
        self.end_time = time.time()
        self.delta_time = self.end_time - self.start_time
        self.wait_time = self.ideal_time - self.delta_time
        if self.wait_time < 0:
            self.wait_time = 0

    def wait(self):
        time.sleep(self.wait_time)
        self.delta_time += self.wait_time
        self.start_time = self.end_time + self.wait_time

    def get_delta_time(self):
        return self.delta_time
