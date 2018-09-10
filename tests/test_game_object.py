import pygame
from unittest import TestCase

from silnik import image
from silnik.rendering.point import Point
from silnik.rendering.shape import Polygon

from bounce.game_object import GameObject
from bounce import image_paths

class TestGameObject(TestCase):
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
        screen = pygame.display.set_mode(size)  # FIXME: decouple GameObject from pygame.display
        img = image.Image.load(image_paths.PLAYER_MAIN)  # some image is needed to construct an GameObject
        self.game_object = GameObject(img)
        self.base_rect = self.game_object.rect

        # Non-overlapping rectangles
        x_offset = self.game_object.rect.width
        y_offset = self.game_object.rect.height
        self.rect_above = self.base_rect.shifted(y_shift=-(10 + y_offset))
        self.rect_below = self.base_rect.shifted(y_shift=10 + y_offset)
        self.rect_left = self.base_rect.shifted(x_shift=-(10 + x_offset))
        self.rect_right = self.base_rect.shifted(x_shift=10 + x_offset)

class TestIsUnder(TestGameObject):
    def test_is_under_is_true_for_rect_above(self):
        self.assertTrue(
            self.game_object.is_under(self.rect_above))

    def test_is_under_is_false_for_rect_below(self):
        self.assertFalse(
            self.game_object.is_under(self.rect_below))

    def test_is_under_is_false_for_rect_on_the_side(self):
        self.assertFalse(
            self.game_object.is_under(self.rect_left))

class TestIsOver(TestGameObject):
    def test_is_true_for_rect_below(self):
        self.assertTrue(
            self.game_object.is_over(self.rect_below))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.game_object.is_over(self.rect_above))

    def test_is_false_for_rect_on_the_side(self):
        self.assertFalse(
            self.game_object.is_over(self.rect_left))

class TestIsToTheRight(TestGameObject):
    def test_is_true_for_rect_on_the_left(self):
        self.assertTrue(
            self.game_object.is_to_the_right(self.rect_left))

    def test_is_false_for_rect_on_the_right(self):
        self.assertFalse(
            self.game_object.is_to_the_right(self.rect_right))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.game_object.is_to_the_right(self.rect_above))

    def test_is_false_for_line_in_the_bottom_left_corner(self):
        corner = Point(
            self.game_object.rect.left,
            self.game_object.rect.bottom)
        
        # Build a line so that the player is on its edge
        line = Polygon([
            corner + Point(-10, -10),
            corner + Point(10, 10)])

        self.assertFalse(
            self.game_object.is_to_the_right(line))

class TestIsToTheLeft(TestGameObject):
    def test_is_true_for_rect_on_the_right(self):
        self.assertTrue(
            self.game_object.is_to_the_left(self.rect_right))

    def test_is_false_for_rect_on_the_left(self):
        self.assertFalse(
            self.game_object.is_to_the_left(self.rect_left))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.game_object.is_to_the_left(self.rect_above))