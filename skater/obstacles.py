import pygame
from pygame.locals import *


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, image_path = None, image = None, x = 0, y = 0):
        super().__init__()

        if image_path != None:
            self.image = pygame.image.load(image_path).convert_alpha()
        else: 
            self.image = image
            self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
               
        
    # collision player bottom - obstacle top
    def is_under(self, other_rect):
        return self.rect.bottom > other_rect.bottom and self.rect.left < other_rect.right and self.rect.right > other_rect.left

    
    # collision player top - obstacle bottom
    def is_over(self, other_rect):
        return self.rect.top < other_rect.top and self.rect.left < other_rect.right and self.rect.right > other_rect.left


    # collision player right - obstacle left
    def is_colliding_right(self, other_rect):
        return self.rect.left >= other_rect.left and self.rect.left <= other_rect.right and self.rect.top < other_rect.bottom

    
    # collision player left - obstacle right
    def is_colliding_left(self, other_rect):
        return self.rect.right >= other_rect.left and self.rect.right <= other_rect.right and self.rect.top < other_rect.bottom
