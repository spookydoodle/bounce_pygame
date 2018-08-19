from unittest import TestCase

from skater.camera import Camera

from .mock_rect import MockRect, shifted

screen_width = 400
screen_height = 300
screen_center_x = screen_width / 2
screen_center_y = screen_height / 2

screen = MockRect(
    0,
    screen_height,
    0,
    screen_width)

# The player is in the center of the screen
base_player = MockRect(
    screen_center_y - 10,
    screen_center_y + 10,
    screen_center_x - 10,
    screen_center_x + 10)

class TestAdjustX(TestCase):
    def test_does_nothing_if_player_in_the_center(self):
        camera = Camera()
        camera.adjust_x(screen, base_player)
        self.assertEqual(camera.x, 0)

    def test_increases_x_if_player_on_the_right(self):
        camera = Camera()
        player = shifted(base_player, x_shift=screen_width)
        camera.adjust_x(screen, player)
        self.assertGreater(camera.x, 0)

    def test_decreases_x_if_player_on_the_left(self):
        camera = Camera()
        player = shifted(base_player, x_shift=-screen_width)
        camera.adjust_x(screen, player)
        self.assertLess(camera.x, 0)

class TestAdjustY(TestCase):
    def test_does_nothing_if_player_in_the_center(self):
        camera = Camera()
        camera.adjust_y(screen, base_player)
        self.assertEqual(camera.y, 0)

    def test_increases_y_if_player_on_the_bottom(self):
        camera = Camera()
        player = shifted(base_player, y_shift=screen_height)
        camera.adjust_y(screen, player)
        self.assertGreater(camera.y, 0)

    def test_decreases_y_if_player_on_the_top(self):
        camera = Camera()
        player = shifted(base_player, y_shift=-screen_height)
        camera.adjust_y(screen, player)
        self.assertLess(camera.y, 0)