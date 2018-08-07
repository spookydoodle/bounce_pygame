import pygame
from pygame.locals import *
from .dicts import *

from skater import images


class Player(pygame.sprite.Sprite):

    # these parameters are used to decrease velocity when decelerating
    DRAG = 0.9
    ZERO = 0.01

    # gravity parameter used for relating jumping velocity to main velocity G * v
    G = 0.9
    
    # elasticity parameter used to decrease velocity when hitting the ground
    ELASTICITY = 0.8

    def __init__(self, speed = 0):
        super().__init__()

        self.image = pygame.image.load(images.PLAYER_MAIN).convert_alpha()
        self.rect = self.image.get_rect()

        # speed is used for movement to left/right
        self.speed = speed

        # acceleration, velocity, mass - used for acceleration and deceleration. 
        # separate velocities for movement on x axis (right/left) and y axis (jump)
        self.v_x = self.v0 = speed * 1.8
        self.v_y = self.G * self.v0
        self.m = 4

        # flags used to perform tricks
        self.is_manual = False

        # these parameters are used to stop the player after hitting  obstacle on horizontal axis (x)
        #self.is_colliding_r = False
        #self.is_colliding_l = False
        self.is_colliding_t = False
        self.is_colliding_b = False

                # these parameters are used to determine direction for accelerating/decelerating when user stops skating; 
        # 1 = right/up, -1 = left/down, 0 = no movement
        self.moving_direction_x = 0
        self.moving_direction_y = 1

    def is_mid_air(self):
        return self.v_y != 0

    def is_jumping(self):
        return self.v_y < 0

    def is_falling(self):
        return self.v_y > 0

    def is_crashed(self):
        return False  # TODO

    # function to load sprite images for each action/trick
    def load_image(self, path):
        self.image = pygame.image.load(path).convert_alpha()

    # handle user input
    def move(self, screen, event, gameboard):
        
        # set moving_direction_x parameter based on user input, except for when skater is in the air
        keystate = pygame.key.get_pressed()

        if not self.is_mid_air():

            # here need to change to also use the dictionary CONTROLS - tbd later
            if (keystate[K_RIGHT] or keystate[K_d]):
                self.moving_direction_x = 1
                self.speed = self.v0

            if (keystate[K_LEFT] or keystate[K_a]) and self.rect.x > 0: 
                self.moving_direction_x = -1
                self.speed = self.v0


        # set flags for tricks based on user input
        if keystate[K_UP]: self.is_manual = True
        else: self.is_manual = False


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
        # update the position according to previously computed speed
        self.rect.x += self.speed * self.moving_direction_x

        # update the speed for the next iteration
        if not self.is_mid_air():
            # decrease velocity using drag parameter but only if on the ground
            self.speed *= self.DRAG

        # if speed is below a threshold, set it to zero
        if self.speed <= self.ZERO:
            self.speed = 0

        # find x position of the closest obstacle edges on the right and left side of the player
        limit_right = min(obstacle.rect.left for obstacle in gameboard.obstacles_right(self))
        limit_left = max(obstacle.rect.right for obstacle in gameboard.obstacles_left(self))
        
        # stop movement if collision on the right of the player takes place
        if self.moving_direction_x > 0 and self.rect.right > limit_right:
            self.stop_movement_x(limit_right - self.rect.width)
        
        # stop movement if collision on the left of the player takes place
        if self.moving_direction_x < 0 and self.rect.left < limit_left:
            self.stop_movement_x(limit_left)
            

    def move_y(self, gameboard):
        if not self.is_colliding_b:
            # Calculate y-acceleration (gravity pull)
            a = self.m * self.G

            # Update y-speed with new acceleration
            self.v_y += a

            # Update y-position
            self.rect.y += self.v_y
            
            # floor is the most top horizontal edge of all obstacles in the gameboard
            floor = min(obstacle.rect.top for obstacle in gameboard.obstacles_under(self))

            floor_hit = self.rect.bottom > floor
            if floor_hit:
                self.stop_movement_y(floor)


    def jump(self):
        self.v_y = -self.v0  * 5 # NOTE: some random number

    def stop_movement_x(self, x):
        self.rect.x = x
        self.moving_direction_x = 0
        self.v_x = 0

    def stop_movement_y(self, y):
        self.rect.bottom = y
        self.v_y = 0

    def handle_images(self):

        if self.is_mid_air() or self.is_manual:
           if self.moving_direction_x >= 0: img = images.PLAYER_MANUAL
           if self.moving_direction_x < 0: img = images.PLAYER_NOSE_MANUAL

        elif self.is_crashed(): img = images.PLAYER_CRASH

        else: self.image = img = images.PLAYER_MAIN
        
        self.image = pygame.image.load(img).convert_alpha()