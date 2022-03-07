from . import filehandler, handler

class State:
    def __init__(self):
        """State class Constructor"""
        self.handler = handler.Handler()