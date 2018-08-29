import pygame
from pygame.locals import *
from .dicts import *

from . import image, image_paths


class Player(pygame.sprite.Sprite):

    # these parameters are used to decrease velocity when decelerating
    DRAG = 0.9
    ZERO = 0.01

    # gravity parameter used for relating jumping velocity to main velocity G * v
    G = 0.9
    
    # elasticity parameter used to decrease velocity when hitting the ground
    ELASTICITY = 0.8

    # factor used to calculate max jump height, used to multiply player's speed unit
    LEAP_FORCE = 5

    def __init__(self, speed_unit=1):
        super().__init__()

        self.speed_unit = speed_unit

        self.image = image.Image.load(image_paths.PLAYER_MAIN)
        self.rect = self.image.shape

        # acceleration, velocity, mass - used for acceleration and deceleration. 
        # separate velocities for movement on x axis (right/left) and y axis (jump)
        self.v_x = 0
        self.v_y = 0
        self.m = 4

        # initial direction - to the left
        self.direction = 'L'


    def is_mid_air(self):
        return self.v_y != 0

    def is_jumping(self):
        return self.v_y < 0

    def is_falling(self):
        return self.v_y > 0

    def is_crashed(self):
        return (self.rect.left < 50 or self.rect.right > 600)

    def is_mid_x(self):
        return self.is_moving_left() or self.is_moving_right()

    def is_moving_right(self):
        return self.v_x > 0

    def is_moving_left(self):
        return self.v_x < 0


    # handle user input
    def move(self, screen, event, gameboard):
        
        keystate = pygame.key.get_pressed()

        if not self.is_mid_x():

            ## here need to change to also use the dictionary CONTROLS - tbd later
            #if (keystate[K_RIGHT] or keystate[K_d]):

            if event.type == pygame.KEYDOWN:

                if event.key in CONTROLS["G_RIGHT"]:
                    self.direction = 'R'
                    self.v_x = self.speed_unit

                if event.key in CONTROLS["G_LEFT"]:
                    self.direction = 'L'
                    self.v_x = - self.speed_unit


            # fall to the right/left if obstacle's end is reached
            if self.direction == 'R' and  not gameboard.is_colliding_right(self):
                self.v_x = self.speed_unit

            if self.direction == 'L' and not gameboard.is_colliding_left(self):
                self.v_x = - self.speed_unit


        # call movement functions after handling user input
        self.call_movement_functions(gameboard)

    
    def call_movement_functions(self, gameboard):
        
        self.move_x(gameboard)
        self.move_y(gameboard)
        self.handle_images()


    def move_x(self, gameboard):
        # find x position of the closest obstacle edges on the right and left side of the player
        # NOTE: this has to be computed *before* modifying self.rect.x
        limit_right = gameboard.limit_right(self)
        limit_left = gameboard.limit_left(self)

        # update the position according to previously computed speed
        self.rect.x += self.v_x
        
        # stop movement if collision on the right/left of the player takes place
        self.check_stop_movement_right(limit_right)
        self.check_stop_movement_left(limit_left)
            
    
    def check_stop_movement_right(self, limit):
        if self.is_moving_right() and self.rect.right > limit:
            self.stop_movement_x(limit - self.rect.width)


    def check_stop_movement_left(self, limit):
        if self.is_moving_left() and self.rect.left < limit:
            self.stop_movement_x(limit)


    def move_y(self, gameboard):
        ## NOTE: this has to be computed *before* modifying self.rect.y
        #floor = gameboard.limit_under(self)

        ## Calculate y-acceleration (gravity pull)
        #a = self.m * self.G

        ## Update y-speed with new acceleration
        #self.v_y += a

        ## Update y-position
        #self.rect.y += self.v_y
            
        #floor_hit = self.rect.bottom > floor
        #if floor_hit:
        #    self.stop_movement_y(floor)

        self.rect.y -= 1


    def jump(self):
        self.v_y = -self.speed_unit * self.LEAP_FORCE

    def stop_movement_x(self, x):
        self.rect.x = x
        self.v_x = 0

    def stop_movement_y(self, y):
        self.rect.bottom = y
        self.v_y = 0

    def handle_images(self):

        if self.is_mid_air():
            if self.is_moving_left():
                img = image_paths.PLAYER_NOSE_MANUAL
            else:
                img = image_paths.PLAYER_MANUAL

        elif self.is_crashed():
            img = image_paths.PLAYER_CRASH

        else:
            img = image_paths.PLAYER_MAIN
        
        self.image = image.Image.load(img)