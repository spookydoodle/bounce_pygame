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
        colliding_objects = self.get_colliding_objects_x(gameboard)
        colliding_objects.sort(key=lambda obj: abs(self.rect.distance_x(obj.rect)))

        if len(colliding_objects) > 0:
            obj = colliding_objects[0]
            self.on_collision_x(obj, gameboard)
            obj.on_collision_x(self, gameboard)
        
        self.rect.x += self.v_x

    def move_y(self, gameboard):
        # Calculate y-acceleration (gravity pull)
        a = self.m * self.G

        # Update y-speed with new acceleration
        self.v_y += a

        # Get all objects on path
        colliding_objects = self.get_colliding_objects_y(gameboard)
        colliding_objects.sort(key=lambda obj: abs(self.rect.distance_y(obj.rect)))
        
        if len(colliding_objects) > 0:
            # Trigger the collision handler for the first object
            # TODO: add some magic to trigger multiple handlers
            obj = colliding_objects[0]
            self.on_collision_y(obj, gameboard)
            obj.on_collision_y(self, gameboard)
    
        # Update y-position
        # This will get executed after calling all `on_collision` handlers
        # If you want to stop `self` after collisions, make sure to set `v_y` to 0 in `on_collision`
        self.rect.y += self.v_y

    def get_colliding_objects_x(self, gameboard):
        """
        Returns a list of objects that will collide with `self` in the current iteration

        # NOTE: `self.v_x` value should be updated *before* calling this method
        """            
        # A function that takes an object and returns a distance in the `x` axis
        distance_function = lambda obj: self.rect.distance_x(obj.rect)

        if self.is_moving_right():
            candidates = gameboard.objects_right(self)
            return [
                obj
                for obj, distance in self._zipped_with(candidates, distance_function)
                if distance < self.v_x
            ]

        elif self.is_moving_left():
            candidates = gameboard.objects_left(self)

            return [
                obj
                for obj, distance in self._zipped_with(candidates, distance_function)
                if distance > self.v_x
            ]

        else:
            return []

    def get_colliding_objects_y(self, gameboard):
        """
        Returns a list of objects that will collide with `self` in the current iteration

        # NOTE: `self.v_y` value should be updated *before* calling this method
        """            
        # A function that takes an object and returns a distance in the `y` axis
        distance_function = lambda obj: self.rect.distance_y(obj.rect)

        if self.is_falling():
            candidates = gameboard.objects_under(self)

            return [
                obj
                for obj, distance in self._zipped_with(candidates, distance_function)
                if distance < self.v_y
            ]

        elif self.is_jumping():
            candidates = gameboard.objects_above(self)

            return [
                obj
                for obj, distance in self._zipped_with(candidates, distance_function)
                if distance > self.v_y
            ]

        else:
            return []

    @staticmethod
    def _zipped_with(objects, func):
        return zip(
            objects,
            [func(obj) for obj in objects])