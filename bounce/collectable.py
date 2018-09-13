from silnik.image import Image

from .constants import Colors
from .game_object import GameObject
from .utils import rect_in_corner

class Collectable(GameObject):
    COLOR = Colors.GREEN

    @classmethod
    def build(cls, size, x=0, y=0):
        shape = rect_in_corner(*size)
        image = Image.create(shape, cls.COLOR)
        return cls(image, x, y)