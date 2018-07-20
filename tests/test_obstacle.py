import pygame
from unittest import TestCase

from skater.obstacles import Obstacle
from skater import images

class MockRect:
    """
    A mock replacement of `pygame.sprite.Sprite.rect` for testing purposes
    """
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    @property
    def x(self):
        return (self.left + self.right) / 2

    @property
    def y(self):
        return (self.top + self.bottom) / 2


class TestObstacle(TestCase):

    def setUp(self):
        size = width, height = (1280, 720)
        screen = pygame.display.set_mode(size)  # FIXME: decouple Obstacle from pygame.display
        image = images.PLAYER_MAIN  # some image is needed to construct an Obstacle
        self.obstacle = Obstacle(image)

    def test_is_under_is_true_for_rect_above(self):
        obstacle_rect = self.obstacle.rect
        rect_above = MockRect(obstacle_rect.top - 10, obstacle_rect.top, obstacle_rect.left, obstacle_rect.right)
        self.assertTrue(self.obstacle.is_under(rect_above))

    def test_is_under_is_false_for_rect_below(self):
        obstacle_rect = self.obstacle.rect
        rect_below = MockRect(obstacle_rect.bottom, obstacle_rect.bottom + 10, obstacle_rect.left, obstacle_rect.right)
        self.assertFalse(self.obstacle.is_under(rect_below))

    def test_is_under_is_false_for_rect_on_the_side(self):
        obstacle_rect = self.obstacle.rect
        rect_on_the_left = MockRect(obstacle_rect.top - 10, obstacle_rect.top, obstacle_rect.left -10, obstacle_rect.left)
        self.assertFalse(self.obstacle.is_under(rect_on_the_left))
