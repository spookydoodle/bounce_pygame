from unittest import TestCase, mock

from silnik.image import Image
from silnik.rendering.point import Point
from silnik.rendering.shape import rectangle

from bounce.gameboard import GameBoard
from bounce.game_object import GameObject
from bounce.moving_object import MovingObject

class TestMovingObject(TestCase):
    """
    Base TestCase to share the setup logic and data
    """
    def setUp(self):
        shape = rectangle(
            Point(0, 0),
            Point(100, 100))
        img = Image("mock_raw_image", shape)
        self.object = MovingObject(img)
        self.base_rect = self.object.rect

    def make_wall(self, x=0, y=0):
        img = Image.create(self.base_rect.clone())
        return GameObject(
            img,
            x=x + self.base_rect.width,
            y=y + self.base_rect.height)

class TestMove(TestMovingObject):
    def setUp(self):
        super().setUp()
        self.object.v_x = 100

    def test_updates_x_position(self):
        distance = self.object.v_x * 1.1  # > self.v_x
        wall_right = self.make_wall(x=distance)
        
        gameboard = GameBoard([wall_right], [], [], [])

        self.object.move_x(gameboard)
        self.assertEqual(
            self.object.rect.x,
            self.object.v_x)

    def test_calls_handler_on_collision(self):
        distance = self.object.v_x * 0.1  # < self.v_x
        wall_right = self.make_wall(x=distance)
        
        gameboard = GameBoard([wall_right], [], [], [])

        expected_direction = 'R'
        expected_location = Point(
            self.base_rect.width + distance - 1,
            0)

        with mock.patch.object(self.object, 'on_collision_x') as mock_collision:
            self.object.move_x(gameboard)
            mock_collision.assert_called_once_with(wall_right)