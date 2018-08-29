import os 
import string
import pygame
from pygame.locals import *
from bounce.game import *
from bounce.menu import *
from bounce.controls import *
from bounce.exit import Exit
from bounce.router import Router
from bounce.destination import Destination
from bounce import image, image_paths

size = width, height = (650, 800)

# Set game window frame, background amd fonts for printing
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(size)

background_image = image.Image.load(image_paths.BACKGROUND)

done = False
clock = pygame.time.Clock()
game_state = Menu()

router = Router({
    Destination.MENU: Menu,
    Destination.CONTROLS: Controls,
    Destination.GAME: Game,
    Destination.EXIT: Exit
})

while not done:

    done = game_state.check_exit()

    destination = game_state.next_destination()

    # reroute only if the current `game_state` pointed to a destination
    if destination:
        game_state = router.route(destination)

    # Get the next queued event 
    event = pygame.event.poll()
    
    game_state.run(screen, event)

    game_state.display_frame(screen, background_image)
    
    # Limit to N frames per second
    clock.tick(60)


pygame.quit()