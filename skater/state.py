import pygame
from pygame.locals import *
from .render_functions import *
from .dicts import *


class State:
    
    def __init__(self):
        self.active_state = ""
        self.exit = False

    def process_events(self):
        raise NotImplementedError
    
    def run(self):
        raise NotImplementedError
    
    def display_frame(self, background_image):
        raise NotImplementedError

    def check_exit(self):
        if self.exit: return True
        else: return False