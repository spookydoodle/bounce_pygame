import pygame
from math import inf
from pygame.locals import *


class GameObject(pygame.sprite.Sprite):

    def __init__(self, image, x = 0, y = 0):
        super().__init__()
        self.image = image
        self.image.shape.x = x
        self.image.shape.y = y

    def is_under(self, other_rect):
        """
        Checks if `self` is located below `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_y(self.image.shape)
        return distance != inf and distance > 0
    
    def is_above(self, other_rect):
        """
        Checks if `self` is located over `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_y(self.image.shape)
        return distance != inf and distance < 0

    def is_to_the_right(self, other_rect):
        """
        Checks if `self` is located to the right of `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_x(self.image.shape)
        return distance != inf and distance > 0

    def is_to_the_left(self, other_rect):
        """
        Checks if `self` is located to the left of `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_x(self.image.shape)
        return distance != inf and distance < 0

    def collides_with(self, other_rect):
        """
        Objects collide if the distances in each axis are smaller than the respective dimension
        """
        distance_x = other_rect.distance_x(self.image.shape)
        distance_y = other_rect.distance_y(self.image.shape)

        return 0 < distance_x < self.image.shape.width and 0 < distance_y < self.image.shape.height

    def on_collision_x(self, object_hit, gameboard):
        pass

    def on_collision_y(self, object_hit, gameboard):
        pass

    def destroy(self, gameboard):
        gameboard.remove(self)