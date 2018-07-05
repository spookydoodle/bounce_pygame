import pygame
from pygame.locals import *
from .dicts import *

from skater import images


class Player(pygame.sprite.Sprite):

    # these parameters are used to decrease velocity when decelerating
    DRAG = 0.7
    ZERO = 0.000001

    # gravity parameter used for relating jumping velocity to main velocity G * v
    G = 0.8
    
    # elasticity parameter used to decrease velocity when hitting the ground
    ELASTICITY = 0.8

    def __init__(self, speed = 0):
        super().__init__()

        self.image = pygame.image.load(images.PLAYER_MAIN).convert_alpha()
        self.rect = self.image.get_rect()

        #self.collider = pygame.transform.scale(self.image, (int(0.6 * self.rect.width), int(0.6 * self.rect.height)))
        #self.collider = self.collider.move((int(0.2 * self.rect.width), int(0.2 * self.rect.height)))
        #self.collider_rect = self.collider.get_rect()

        # speed is used for movement to left/right
        self.speed = speed

        # acceleration, velocity, mass - used for acceleration and deceleration. 
        # separate velocities for movement on x axis (right/left) and y axis (jump)
        self.a = 2
        self.v = self.v0 = 8
        self.v_jump = self.G * self.v0
        self.m = 5
        self.is_jumping = False
        self.is_falling = False
        self.is_decelerating = False

        # flags used to perform tricks
        self.is_manual = False

        # these parameters are used to stop the player after hitting  obstacle on horizontal axis (x)
        self.is_colliding_r = False
        self.is_colliding_l = False
        self.is_colliding_t = False
        self.is_colliding_b = False

                # these parameters are used to determine direction for accelerating/decelerating when user stops skating; 
        # 1 = right/up, -1 = left/down, 0 = no movement
        self.moving_direction_x = 0
        self.moving_direction_y = 1


    # function to load sprite images for each action/trick
    def load_image(self, path):
        self.image = pygame.image.load(path).convert_alpha()

    # handle user input
    def move(self, screen, events):
        
        # set moving_direction_x parameter based on user input, except for when skater is in the air (is_jumping parameter)
        keystate = pygame.key.get_pressed()

        if not self.is_jumping:

            # here need to change to also use the dictionary CONTROLS - tbd later
            if (keystate[K_RIGHT] or keystate[K_d]) and self.rect.x < (screen.get_size()[0] - self.rect.width):
                self.moving_direction_x = 1

            if (keystate[K_LEFT] or keystate[K_a]) and self.rect.x > 0: 
                self.moving_direction_x = -1


        # set flags for tricks based on user input
        if keystate[K_UP]: self.is_manual = True
        else: self.is_manual = False


        # set flags for jumping based on user input and for deceleration if user stops pressing movement buttons
        for event in events:
            if event.type == pygame.KEYDOWN:
                #if event.key in [CONTROLS["G_RIGHT"], CONTROLS["G_LEFT"]]:
                #    self.stop_movement_x()

                if event.key in CONTROLS["G_OLLIE"]:
                    self.is_jumping = True

            elif event.type == pygame.KEYUP:
                self.is_decelerating = True
                self.is_manual = False


        # call movement functions after handling user input
        self.call_movement_functions()

    
    def call_movement_functions(self):
        self.accelerate()
        self.decelerate()
        self.handle_images()


    def accelerate(self):
        if (not self.is_colliding_r and self.moving_direction_x > 0) \
        or (not self.is_colliding_l and self.moving_direction_x < 0):
            self.rect.x += self.speed * self.moving_direction_x
            #self.rect.x += self.v * self.v / self.a * self.moving_direction_x

            #if self.v < 10:
            #    self.v *= 1.2
        

    def decelerate(self):

        if not self.is_colliding_r:

            if self.v > self.ZERO and self.is_decelerating:
                self.rect.x += self.v * self.v / self.a * self.moving_direction_x
            
                # decrease velocity using drag parameter but only if on the ground
                if not self.is_jumping:
                    self.v *= self.DRAG 

            # if velocity reaches 0.00001 reset to initial velocity value v0
            elif self.v <= self.ZERO:
                self.stop_movement_x()



    def jump(self):
        if self.is_jumping:
            # Calculate force (F)
            F = self.m * self.v_jump
            
            # Change position
            self.rect.y -= F
 
            # Change velocity
            self.v_jump -= 1


            ## this code was supposed to make jumps smoother

            #if not self.is_falling:
            #    self.v_jump *= self.DRAG
            #else:
            #    self.v_jump = (-1) * abs(self.v_jump) * 1/self.DRAG

            #if self.v_jump < self.ZERO:
            #    self.is_falling = True


            ## If ground is reached, reset variables.
            #if self.rect.y >= ground_pos_y:
            #    self.stop_movement_y()

    
    def fall(self):
        if not self.is_colliding_b:
            self.rect.y += self.m * self.G


    def stop_movement_x(self):
        self.is_decelerating = False
        self.moving_direction_x = 0
        self.v = self.v0

    
    def stop_movement_y(self, y):
        self.rect.y = y
        self.v_jump = self.G * self.v0
        self.v *= self.ELASTICITY
        self.is_jumping = False
        self.is_falling = False


    def handle_images(self):
        if self.is_manual: self.image = pygame.image.load(images.PLAYER_MANUAL).convert_alpha()
        else: self.image = pygame.image.load(images.PLAYER_MAIN).convert_alpha()