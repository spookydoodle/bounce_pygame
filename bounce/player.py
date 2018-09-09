import pygame
from pygame.locals import *
from .game_object import *
from .moving_object import MovingObject

from silnik import image
from silnik.rendering.shape import Polygon, rectangle
from silnik.rendering.point import Point

from .constants import *
from . import image_paths


class Player(MovingObject):

    # factor used to calculate max jump height, used to multiply player's speed unit
    LEAP_FORCE = 5

    def __init__(self, speed_unit=1):
        img = image.Image.load(image_paths.PLAYER_MAIN)
        super().__init__(image=img, speed_unit=speed_unit)

        # acceleration, velocity, mass - used for acceleration and deceleration. 
        # separate velocities for movement on x axis (right/left) and y axis (jump)
        self.v_x = 0
        self.v_y = - self.speed_unit/3
        self.m = 4

        # initial direction - to the left
        self.direction = 'L'

    def is_crashed(self):
        return (self.rect.left < 50 or self.rect.right > 600)

    # handle user input
    # TODO: rename this method
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
            # FIXME: commented out because `gameboard` implementation is not yet ready
            if self.direction == 'R' and  not gameboard.is_colliding_wall_right(self):
                self.v_x = self.speed_unit

            if self.direction == 'L' and not gameboard.is_colliding_wall_left(self):
                self.v_x = - self.speed_unit


        # call movement functions after handling user input
        self.call_movement_functions(gameboard)
        self.handle_images()

    def on_collision(self, location, direction, object_hit=None):
        if direction == 'U':
            self.stop_movement_y(location.y)
        elif direction == 'D':
            self.stop_movement_y(location.y - self.rect.height)
        elif direction == 'L':
            self.stop_movement_x(location.x)
        elif direction == 'R':
            self.stop_movement_x(location.x - self.rect.width)

    def jump(self):
        self.v_y = -self.speed_unit * self.LEAP_FORCE

    def stop_movement_x(self, x):
        self.rect.x = x
        self.v_x = 0

    def stop_movement_y(self, y):
        self.rect.bottom = y
        self.v_y = 0

    def handle_images(self):

        #if self.is_mid_x():
        if self.is_crashed():
            img = image_paths.PLAYER_CRASH
        
        elif self.is_moving_right():
            img = image_paths.PLAYER_MOVE_RIGHT

        elif self.is_moving_left():
            img = image_paths.PLAYER_MOVE_LEFT

        else:
            img = image_paths.PLAYER_MAIN
        
        self.image = image.Image.load(img)

     
    def append_bullet(self, event, gameboard, width = 5):

        if event.type == pygame.KEYDOWN:

            if event.key in CONTROLS["G_SHOOT"]:
                gameboard.bullets.append(self.create_bullet(
                    (width, width * 1.5),
                    x = (self.rect.left + self.rect.right) / 2 - width / 2,
                    y = self.rect.top))

    def create_bullet(self, size, x, y):
        shape = rectangle(Point(0, 0), Point(*size))
        return GameObject(
            image = image.Image.create(shape, color = Colors.MAGENTA ),
            x = x,
            y = y)

    def move_bullets(self, gameboard, bullet_speed):
        for bullet in gameboard.bullets:
            bullet.rect.y -= bullet_speed