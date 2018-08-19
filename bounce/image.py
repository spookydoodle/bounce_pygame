import random

import pygame

class Image:
    """
    A wrapper around a pygame image class. It provides a common interface for
    drawable elements.

    The code outside of this class should not use any other image-related APIs.

    `self.shape` is a pygame.rect instance for now.
    Will be replaced by another class once non-rectangular shapes are supported
    """
    def __init__(self, raw_image):
        self.raw_image = raw_image
        self.shape = raw_image.get_rect()

    @classmethod
    def load(cls, path):
        """
        Loads and prepares an image from a local file
        """
        return Image(pygame.image.load(path).convert_alpha())

    @classmethod
    def create(cls, size, color=None):
        """
        Creates a new rectangular surface
        """
        # If no color was specified, just create a random one
        color = color or cls.random_color()

        surface = pygame.Surface(size)
        surface.fill(color)
        return Image(surface)

    @staticmethod
    def random_color():
        # colors are integers of value <0, 255>
        lo = 0
        hi = 255

        return [
            random.randint(lo, hi)
            for _ in range(3)
        ]