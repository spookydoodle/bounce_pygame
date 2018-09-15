from silnik.image import Image

from .constants import Colors
from .game_object import GameObject
from .utils import rect_in_corner

class Obstacle(GameObject):
    COLOR = Colors.RED

    @classmethod
    def build(cls, size, x=0, y=0):
        shape = rect_in_corner(*size)
        image = Image.create(shape, cls.COLOR)
        return cls(image, x, y)

    def on_collision_x(self, object_hit, gameboard):
        from .bullet import Bullet  # import here to avoid a circular dependency on start (kinda hacky)
        if isinstance(object_hit, Bullet):
            self.destroy(gameboard)

    def on_collision_y(self, object_hit, gameboard):
        from .bullet import Bullet  # import here to avoid a circular dependency on start (kinda hacky)
        if isinstance(object_hit, Bullet):
            self.destroy(gameboard)