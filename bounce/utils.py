from silnik.rendering.shape import rectangle
from silnik.rendering.point import Point

def rect_in_corner(width, height):
    top_left = Point(0, 0)
    bottom_right = Point(width, height)
    return rectangle(top_left, bottom_right)