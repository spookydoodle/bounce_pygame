import pygame

from silnik import image
from silnik.rendering.shape import Polygon, rectangle
from silnik.rendering.point import Point

from .game_object import GameObject
from .moving_object import MovingObject
from .constants import Colors, CONTROLS
from . import image_paths


class Player(MovingObject):

    def __init__(self, speed_unit=1):
        img = image.Image.load(image_paths.PLAYER_MAIN)
        super().__init__(image=img, speed_unit=speed_unit, v_x0=-speed_unit, v_y0=-speed_unit/3, m=4)

        self.store_last_movement_direction()

    def is_crashed(self):
        return (self.rect.left < 50 or self.rect.right > 600)

    def process_event(self, event):

        if event.type == pygame.KEYDOWN and not self.is_mid_x():

            if event.key in CONTROLS["G_RIGHT"]:
                self.v_x = self.speed_unit

            elif event.key in CONTROLS["G_LEFT"]:
                self.v_x = - self.speed_unit

    def move(self, gameboard):
        self.store_last_movement_direction()

        if self._last_movement_direction == 'R' and  not gameboard.is_colliding_wall_right(self):
            self.v_x = self.speed_unit

        elif self._last_movement_direction == 'L' and not gameboard.is_colliding_wall_left(self):
            self.v_x = -self.speed_unit

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

    def stop_movement_x(self, x):
        self.rect.x = x
        self.v_x = 0

    def stop_movement_y(self, y):
        self.rect.bottom = y
        self.v_y = 0

    def handle_images(self):
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
        # TODO: create a `Bullet` class, derive from `MovingObject`, let it handle its own movement
        for bullet in gameboard.bullets:
            bullet.rect.y -= bullet_speed

    def store_last_movement_direction(self):
        # don't update if `self` is not currently moving
        if self.v_x == 0:
            pass
        else:
            direction = 'L' if self.v_x < 0 else 'R'
            self._last_movement_direction = direction