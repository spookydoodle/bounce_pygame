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
        return (self.left + self.right)

    @property
    def y(self):
        return (self.top + self.bottom)

    @property
    def width(self):
        return (self.right - self.left)

    @property
    def height(self):
        return (self.bottom - self.top)

# Utility methods to make tests more readable
def makeMockRect(other_rectangle):
    return MockRect(
        other_rectangle.top,
        other_rectangle.bottom,
        other_rectangle.left,
        other_rectangle.right
    )

def shifted(base_rect, x_shift=0, y_shift=0):
    return MockRect(
        base_rect.top + y_shift,
        base_rect.bottom + y_shift,
        base_rect.left + x_shift,
        base_rect.right + x_shift
    )

class TestObstacle(TestCase):
    """
    Base TestCase class -> all tests will share the same setup logic
    """
    def setUp(self):
        """
        This is the code that will get executed before every test.
   
        Resets the state for each test case, which in turn decouples
        tests from each other.
        """
        size = width, height = (1280, 720)
        screen = pygame.display.set_mode(size)  # FIXME: decouple Obstacle from pygame.display
        image = images.PLAYER_MAIN  # some image is needed to construct an Obstacle
        self.obstacle = Obstacle(image)
        self.base_rect = makeMockRect(self.obstacle.rect)

        # Overlapping rectangles
        self.rect_above = shifted(self.base_rect, y_shift=-10)
        self.rect_below = shifted(self.base_rect, y_shift=10)
        self.rect_left = shifted(self.base_rect, x_shift=-10)
        self.rect_right = shifted(self.base_rect, x_shift=10)

        # Non-overlapping rectangles
        x_offset = self.obstacle.rect.width
        y_offset = self.obstacle.rect.height
        self.rect_far_above = shifted(self.base_rect, y_shift=-(10 + y_offset))
        self.rect_far_below = shifted(self.base_rect, y_shift=10 + y_offset)
        self.rect_far_left = shifted(self.base_rect, x_shift=-(10 + x_offset))
        self.rect_far_right = shifted(self.base_rect, x_shift=10 + x_offset)

class TestIsUnder(TestObstacle):
    def test_is_under_is_true_for_rect_above(self):
        self.assertTrue(
            self.obstacle.is_under(self.rect_above))

    def test_is_under_is_false_for_rect_below(self):
        self.assertFalse(
            self.obstacle.is_under(self.rect_below))

    def test_is_under_is_false_for_rect_on_the_side(self):
        self.assertFalse(
            self.obstacle.is_under(self.rect_left))

class TestIsOver(TestObstacle):
    def test_is_true_for_rect_below(self):
        self.assertTrue(
            self.obstacle.is_over(self.rect_below))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.obstacle.is_over(self.rect_above))

    def test_is_false_for_rect_on_the_side(self):
        self.assertFalse(
            self.obstacle.is_over(self.rect_left))

class TestIsToTheRight(TestObstacle):
    def test_is_true_for_rect_on_the_left(self):
        self.assertTrue(
            self.obstacle.is_to_the_right(self.rect_left))

    def test_is_false_for_rect_on_the_right(self):
        self.assertFalse(
            self.obstacle.is_to_the_right(self.rect_right))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.obstacle.is_to_the_right(self.rect_above))

class TestIsToTheLeft(TestObstacle):
    def test_is_true_for_rect_on_the_right(self):
        self.assertTrue(
            self.obstacle.is_to_the_left(self.rect_right))

    def test_is_false_for_rect_on_the_left(self):
        self.assertFalse(
            self.obstacle.is_to_the_left(self.rect_left))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.obstacle.is_to_the_left(self.rect_above))

class TestIsCollidingRight(TestObstacle):
    def test_is_true_for_rect_overlapping_on_the_right(self):
        self.assertTrue(
            self.obstacle.is_colliding_right(self.rect_right))

    def test_is_false_for_rect_far_to_the_right(self):
        self.assertFalse(
            self.obstacle.is_colliding_right(self.rect_far_right))

    def test_is_false_for_rect_overlapping_on_the_left(self):
            self.assertFalse(
                self.obstacle.is_colliding_right(self.rect_left))

    def test_is_false_for_rect_far_above(self):
            self.assertFalse(
                self.obstacle.is_colliding_right(self.rect_far_above))

class TestIsCollidingLeft(TestObstacle):
    def test_is_true_for_rect_overlapping_on_the_left(self):
        self.assertTrue(
            self.obstacle.is_colliding_left(self.rect_left))

    def test_is_false_for_rect_far_to_the_left(self):
        self.assertFalse(
            self.obstacle.is_colliding_left(self.rect_far_left))

    def test_is_false_for_rect_overlapping_on_the_right(self):
            self.assertFalse(
                self.obstacle.is_colliding_left(self.rect_right))

    def test_is_false_for_rect_far_above(self):
            self.assertFalse(
                self.obstacle.is_colliding_left(self.rect_far_above))