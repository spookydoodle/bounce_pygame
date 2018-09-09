from silnik.rendering.point import Point

from .game_object import GameObject

class MovingObject(GameObject):
    """
    Base class for all `GameObjects` that may move.

    Implements logic related to displacement and a priori
    collision detection.
    """

    # gravity parameter used for relating jumping velocity to main velocity G * v
    G = 0  # set to 0 for now -> update to a positive value after implementing horizontal walls

    def __init__(self, image, x=0, y=0, v_x0=0, v_y0=0, m=0, speed_unit=1):
        # TODO: wrap these parameters in an object / class
        super().__init__(image=image, x=x, y=y)

        self.speed_unit = speed_unit
        self.v_x = v_x0
        self.v_y = v_y0
        self.m = m

    def is_mid_air(self):
        return self.v_y != 0

    def is_jumping(self):
        return self.v_y < 0

    def is_falling(self):
        return self.v_y > 0

    def is_mid_x(self):
        return self.is_moving_left() or self.is_moving_right()

    def is_moving_right(self):
        return self.v_x > 0

    def is_moving_left(self):
        return self.v_x < 0

    def call_movement_functions(self, gameboard):
        self.move_x(gameboard)
        self.move_y(gameboard)

    def move_x(self, gameboard):
        # find x position of the closest obstacle edges on the right and left side of the player
        limit_right = gameboard.limit_right(self)
        limit_left = gameboard.limit_left(self)

        # stop movement if collision on either side of the player takes place
        if self.is_moving_right() and self.v_x > limit_right:
            wall = self.rect.right + limit_right
            self.on_collision(
                location=Point(wall, self.rect.y),
                direction='R')
        
        elif self.is_moving_left() and self.v_x < limit_left:
            wall = self.rect.left + limit_left
            self.on_collision(
                location=Point(wall, self.rect.y),
                direction='L')
        
        else:
            # Free movement -> update the position based on the speed
            self.rect.x += self.v_x

    def move_y(self, gameboard):
        limit = gameboard.limit_under(self)

        # Calculate y-acceleration (gravity pull)
        a = self.m * self.G

        # Update y-speed with new acceleration
        self.v_y += a

        will_hit_floor = self.v_y > limit

        if will_hit_floor:
            floor = self.rect.bottom + limit
            self.on_collision(
                location=Point(self.rect.x, floor),
                direction='U')
        else:
            # Update y-position
            self.rect.y += self.v_y

    def on_collision(self, location, direction, object_hit=None):
        # TODO: refactor move_x/y a bit to get a reference to the
        # colliding object (the `object_hit` variable) and the
        # proper location (the current one is an approximation)
        message = "{} needs to implement the `on_collision` method!".format(
            self.__class__.__name__)

        raise NotImplementedError(message)
