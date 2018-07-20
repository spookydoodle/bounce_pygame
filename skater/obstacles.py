import pygame
from pygame.locals import *
from .dicts import *


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

    def is_under(self, other_rect):
        return self.rect.bottom > other_rect.bottom and self.rect.left < other_rect.right and self.rect.right > other_rect.left
