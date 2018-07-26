import os 
import string
import pygame
from pygame.locals import *
from skater.game import *
from skater.menu import *
from skater.controls import *
from skater import images


# Set fonts for drawing 
pygame.init()
pygame.font.init() 

# Set game window frame, background amd fonts for printing
background_image = pygame.image.load(images.BACKGROUND)
##size = width, height = background_image.get_rect().width, background_image.get_rect().height
size = width, height = (1280, 720)
screen = pygame.display.set_mode(size)
##screen.blit(background_image, (0, 0))

done = False
clock = pygame.time.Clock()
game_state = Menu()

while not done:

    done = game_state.check_exit()

    if game_state.__class__ != game_state.process_events().__class__: 
        game_state = game_state.process_events()

    # Get the next queued event 
    event = pygame.event.poll()
    
    game_state.run(screen, event)

    game_state.display_frame(screen, background_image)
    
    # Limit to N frames per second
    clock.tick(90)


pygame.quit()