import pygame
from unittest import TestCase

from skater.image import Image

class TestCreate(TestCase):
    def test_creates_a_rectangle_of_correct_size(self):
        color = (0, 0, 0)
        shape = (100, 200)
        
        got = Image.create(shape, color)

        self.assertEqual(
            (got.shape.width, got.shape.height),
            shape)