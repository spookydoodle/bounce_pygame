import pygame

from silnik import image
from silnik.rendering.shape import Polygon, rectangle
from silnik.rendering.point import Point

from .game_object import GameObject
from .moving_object import MovingObject
from .constants import Colors


class Bullet(MovingObject):

    def __init__(self, x=0, y=0, width=5):
        shape = rectangle(
            Point(0, 0),
            Point(width, width * 1.5))
        img = image.Image.create(shape, color = Colors.MAGENTA)
        super().__init__(x=x, y=y, v_y0=-12, image=img)

    def move(self, gameboard):
        self.call_movement_functions(gameboard)

    def on_collision_x(self, object_hit):
        print("Bullet collision x with {}".format(object_hit))

    def on_collision_y(self, object_hit):
        print("Bullet collision y with {}".format(object_hit))