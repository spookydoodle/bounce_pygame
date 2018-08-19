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

        # flags used to perform tricks
        self.is_manual = False


    def is_mid_air(self):
        return self.v_y != 0

    def is_jumping(self):
        return self.v_y < 0

    def is_falling(self):
        return self.v_y > 0

    def is_crashed(self):
        return False  # TODO

    def is_moving_right(self):
        return self.v_x > 0

    def is_moving_left(self):
        return self.v_x < 0

    # handle user input
    def move(self, screen, event, gameboard):
        
        keystate = pygame.key.get_pressed()

        if not self.is_mid_air():

            ## here need to change to also use the dictionary CONTROLS - tbd later
            #if (keystate[K_RIGHT] or keystate[K_d]):

            if event.type == pygame.KEYDOWN:
            #if event.key in [CONTROLS["G_RIGHT"], CONTROLS["G_LEFT"]]:
            #    self.stop_movement_x()

                if event.key in CONTROLS["G_RIGHT"]:
                    self.v_x = self.speed_unit

                if event.key in CONTROLS["G_LEFT"]:
                    self.v_x = - self.speed_unit

            #if (keystate[K_LEFT] or keystate[K_a]) and self.rect.x > 0: 
            #    self.v_x = - self.speed_unit


        ## set flags for tricks based on user input
        #if keystate[K_UP]: self.is_manual = True
        #else: self.is_manual = False


        # set flags for jumping based on user input and for deceleration if user stops pressing movement buttons
        if event.type == pygame.KEYDOWN:
            #if event.key in [CONTROLS["G_RIGHT"], CONTROLS["G_LEFT"]]:
            #    self.stop_movement_x()

            if event.key in CONTROLS["G_OLLIE"]:
                self.jump()

        elif event.type == pygame.KEYUP:
            self.is_manual = False


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

        ## update the speed for the next iteration
        #if not self.is_mid_air():
        #    # decrease velocity using drag parameter but only if on the ground
        #    self.v_x *= self.DRAG

        # if speed is below a threshold, set it to zero
        if abs(self.v_x) <= self.ZERO:
            self.v_x = 0
        
        # stop movement if collision on the right of the player takes place
        if self.is_moving_right() and self.rect.right > limit_right:
            self.stop_movement_x(limit_right - self.rect.width)
        
        # stop movement if collision on the left of the player takes place
        if self.is_moving_left() and self.rect.left < limit_left:
            self.stop_movement_x(limit_left)
            

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

        if self.is_mid_air() or self.is_manual:
            if self.is_moving_left():
                img = image_paths.PLAYER_NOSE_MANUAL
            else:
                img = image_paths.PLAYER_MANUAL

        elif self.is_crashed():
            img = image_paths.PLAYER_CRASH

        else:
            img = image_paths.PLAYER_MAIN
        
        self.image = image.Image.load(img)