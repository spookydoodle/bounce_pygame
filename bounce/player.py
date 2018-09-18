import pygame

from silnik import image
from silnik.rendering.shape import Polygon, rectangle
from silnik.rendering.point import Point

from .bullet import Bullet
from .game_object import GameObject
from .moving_object import MovingObject
from .constants import Colors, CONTROLS
from . import image_paths


class Player(MovingObject):

    def __init__(self, speed_unit=1, on_obstacle_collision=None, on_collectable_collision=None):
        # External functions to call when specific collisions happen
        self.on_collectable_collision = on_collectable_collision or self._do_nothing
        self.on_obstacle_collision = on_obstacle_collision or self._do_nothing

        img = image.Image.load(image_paths.PLAYER_MAIN)
        super().__init__(image=img, speed_unit=speed_unit, v_x0=-speed_unit, v_y0=-speed_unit/3, m=4)

        self.store_last_movement_direction()

    @staticmethod
    def _do_nothing():
        pass

    def is_crashed(self):
        return False
        return (self.rect.left < 50 or self.rect.right > 600)

    def process_event(self, event):

        if event.type == pygame.KEYDOWN and not self.is_mid_x():

            if event.key in CONTROLS["G_RIGHT"]:
                self.v_x = self.speed_unit

            elif event.key in CONTROLS["G_LEFT"]:
                self.v_x = - self.speed_unit

    def move(self, gameboard):
        self.store_last_movement_direction()

        if self._last_movement_direction == 'R' and not gameboard.is_colliding_wall_right(self):
            self.v_x = self.speed_unit

        elif self._last_movement_direction == 'L' and not gameboard.is_colliding_wall_left(self):
            self.v_x = -self.speed_unit

        self.call_movement_functions(gameboard)
        self.handle_images()

    def on_collision_y(self, object_hit, gameboard):
        distance = self.rect.distance_y(object_hit.rect)
        location = self.rect.y + distance
        self.call_external_collision_handlers(object_hit)
        
        if distance < 0:  # player must've been going up
            self.stop_movement_y(location + 1)
        else:
            self.stop_movement_y(location - 1)

    def on_collision_x(self, object_hit, gameboard):
        distance = self.rect.distance_x(object_hit.rect)
        location = self.rect.x + distance
        self.call_external_collision_handlers(object_hit)

        if distance < 0:  # player must've been going left
            self.stop_movement_x(location + 1)
        else:
            self.stop_movement_x(location - 1)

    def call_external_collision_handlers(self, object_hit):
        from .collectable import Collectable
        from .obstacle import Obstacle
        if isinstance(object_hit, Collectable):
            self.on_collectable_collision()
        if isinstance(object_hit, Obstacle):
            self.on_obstacle_collision()

    def stop_movement_x(self, x):
        self.rect.x = x
        self.v_x = 0

    def stop_movement_y(self, y):
        self.rect.y = y

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
                
                bullet = Bullet(
                    x = (self.rect.left + self.rect.right) / 2 - width / 2,
                    y = self.rect.top)
                
                gameboard.bullets.append(bullet)

    def store_last_movement_direction(self):
        # don't update if `self` is not currently moving
        if self.v_x == 0:
            pass
        else:
            direction = 'L' if self.v_x < 0 else 'R'
            self._last_movement_direction = direction