import pygame

from .state import State

class Exit(State):

    def next_destination(self):
        pygame.quit()            
    
    def run(self, screen, event): 
        pass

    def display_frame(self, screen, background_image):
        pass