import time


FPS = 0
delta_time = 0
start_time = 0
end_time = 0
wait_time = 0
frame_time = 0


def start(fps=30):
    """Start clock"""
    global delta_time, start_time, end_time, frame_time, FPS
    FPS = fps
    frame_time = 1/fps
    delta_time = 0
    start_time = time.time()
    end_time = start_time


def update():
    """Update clock and delta time"""
    global delta_time, start_time, end_time, wait_time, frame_time
    end_time = time.time()
    delta_time = end_time - start_time
    start_time = end_time
    # find wait time
    wait_time = frame_time - delta_time
    if wait_time > 0:
        delta_time += wait_time
        time.sleep(wait_time)