import pygame
from math import inf
from pygame.locals import *


class GameObject(pygame.sprite.Sprite):

    def __init__(self, image, x = 0, y = 0):
        super().__init__()
        self.image = image
        self.rect = self.image.shape
        self.rect.x = x
        self.rect.y = y

    def is_under(self, other_rect):
        """
        Checks if `self` is located below `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_y(self.rect)
        return distance != inf and distance > 0
    
    def is_above(self, other_rect):
        """
        Checks if `self` is located over `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_y(self.rect)
        return distance != inf and distance < 0

    def is_to_the_right(self, other_rect):
        """
        Checks if `self` is located to the right of `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_x(self.rect)
        return distance != inf and distance > 0

    def is_to_the_left(self, other_rect):
        """
        Checks if `self` is located to the left of `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_x(self.rect)
        return distance != inf and distance < 0

    def collides_with(self, other_rect):
        """
        Objects collide if the distances in each axis are smaller than the respective dimension
        """
        distance_x = other_rect.distance_x(self.rect)
        distance_y = other_rect.distance_y(self.rect)

        return 0 < distance_x < self.rect.width and 0 < distance_y < self.rect.height