from unittest import TestCase

from silnik.image import Image
from silnik.rendering.point import Point
from silnik.rendering.shape import Polygon, rectangle

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
        shape = rectangle(
            Point(0, 0),
            Point(100, 100))
        img = Image("mock_raw_image", shape)
        self.object = GameObject(img)
        self.base_rect = self.object.rect

        # Non-overlapping rectangles
        x_offset = self.object.rect.width
        y_offset = self.object.rect.height
        self.rect_above = self.base_rect.shifted(y_shift=-(10 + y_offset))
        self.rect_below = self.base_rect.shifted(y_shift=10 + y_offset)
        self.rect_left = self.base_rect.shifted(x_shift=-(10 + x_offset))
        self.rect_right = self.base_rect.shifted(x_shift=10 + x_offset)

class TestIsUnder(TestGameObject):
    def test_is_under_is_true_for_rect_above(self):
        self.assertTrue(
            self.object.is_under(self.rect_above))

    def test_is_under_is_false_for_rect_below(self):
        self.assertFalse(
            self.object.is_under(self.rect_below))

    def test_is_under_is_false_for_rect_on_the_side(self):
        self.assertFalse(
            self.object.is_under(self.rect_left))

class TestIsAbove(TestGameObject):
    def test_is_true_for_rect_below(self):
        self.assertTrue(
            self.object.is_above(self.rect_below))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.object.is_above(self.rect_above))

    def test_is_false_for_rect_on_the_side(self):
        self.assertFalse(
            self.object.is_above(self.rect_left))

class TestIsToTheRight(TestGameObject):
    def test_is_true_for_rect_on_the_left(self):
        self.assertTrue(
            self.object.is_to_the_right(self.rect_left))

    def test_is_false_for_rect_on_the_right(self):
        self.assertFalse(
            self.object.is_to_the_right(self.rect_right))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.object.is_to_the_right(self.rect_above))

    def test_is_false_for_line_in_the_bottom_left_corner(self):
        corner = Point(
            self.object.rect.left,
            self.object.rect.bottom)
        
        # Build a line so that the player is on its edge
        line = Polygon([
            corner + Point(-10, -10),
            corner + Point(10, 10)])

        self.assertFalse(
            self.object.is_to_the_right(line))

class TestIsToTheLeft(TestGameObject):
    def test_is_true_for_rect_on_the_right(self):
        self.assertTrue(
            self.object.is_to_the_left(self.rect_right))

    def test_is_false_for_rect_on_the_left(self):
        self.assertFalse(
            self.object.is_to_the_left(self.rect_left))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.object.is_to_the_left(self.rect_above))