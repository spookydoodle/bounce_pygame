import pygame
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
        return self.rect.bottom > other_rect.bottom \
            and self.rect.left < other_rect.right \
            and self.rect.right > other_rect.left 

    
    def is_over(self, other_rect):
        """
        Checks if `self` is located over `other_rect`, regardless of the distance
        """
        return self.rect.top <= other_rect.bottom and self.rect.top < other_rect.top \
            and self.rect.left < other_rect.right and self.rect.right > other_rect.left

    def is_to_the_right(self, other_rect):
        """
        Checks if `self` is located to the right of `other_rect`, regardless of the distance
        """
        return self.rect.right > other_rect.right and self.rect.right > other_rect.left \
            and self.rect.top < other_rect.bottom and self.rect.bottom > other_rect.top

    def is_to_the_left(self, other_rect):
        """
        Checks if `self` is located to the left of `other_rect`, regardless of the distance
        """
        return self.rect.left < other_rect.left and self.rect.left < other_rect.right \
            and self.rect.top < other_rect.bottom and self.rect.bottom > other_rect.top

    def is_colliding_right(self, other_rect):
        """
        Checks for a collision (overlap) on the right border of `self`

        (collision player right - obstacle left)
        """
        return self.rect.right >= other_rect.left and self.rect.right <= other_rect.right \
            and self.rect.bottom <= other_rect.bottom and self.rect.bottom >= other_rect.top
    
    def is_colliding_left(self, other_rect):
        """
        Checks for a collision (overlap) on the left border of `self`

        (collision player left - obstacle right)
        """
        return self.rect.left <= other_rect.right and self.rect.left >= other_rect.left \
            and self.rect.bottom <= other_rect.bottom and self.rect.bottom >= other_rect.top