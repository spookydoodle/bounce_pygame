import os 
import string
import pygame
from pygame.locals import *
from cls.game import *


# Set fonts for drawing 
pygame.init()
pygame.font.init() 

# Set game window frame, background amd fonts for printing
background_image = pygame.image.load("graphics/background_image.png")
##size = width, height = background_image.get_rect().width, background_image.get_rect().height
size = width, height = (1280, 720)
screen = pygame.display.set_mode(size)
##screen.blit(background_image, (0, 0))

##Keyword.initialize_list()

done = False
clock = pygame.time.Clock()
game_state = Menu()

while not done:

    done = game_state.check_exit()

    events = pygame.event.get()

    if game_state.__class__ != game_state.process_events().__class__: 
        game_state = game_state.process_events()
    
    game_state.run(screen, events)

    game_state.display_frame(screen, background_image)
    
    clock.tick(60)


pygame.quit()