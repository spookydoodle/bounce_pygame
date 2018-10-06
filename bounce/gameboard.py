from .bullet import Bullet
from .collectable import Collectable
from .obstacle import Obstacle
from .wall import Wall

class GameBoard:
    # infinities to avoid crashes on empty sequence computations
    MIN_POSITION = -2 ** 31
    MAX_POSITION = 2 ** 31

    def __init__(self, walls, collectables, obstacles, bullets):
        self.walls = walls
        self.collectables = collectables
        self.obstacles = obstacles
        self.bullets = bullets

    def of_type(self, type):
        """
        Filters access to a subset of known objects based on `type`
        """
        grouped_by_type = {
            Bullet: self.bullets,
            Collectable: self.collectables,
            Obstacle: self.obstacles,
            Wall: self.walls
        }
        return grouped_by_type[type]

    def all_objects(self):
        return self.walls + self.collectables + self.obstacles + self.bullets

    def objects_under(self, player):
        return [
            obj
            for obj in self.all_objects()
            if obj.is_under(player.image.shape)
        ]

    def objects_above(self, player):
        return [
            obj
            for obj in self.all_objects()
            if obj.is_above(player.image.shape)
        ]

    def objects_left(self, player):
        return [
            obj
            for obj in self.all_objects()
            if obj.is_to_the_left(player.image.shape)
        ]

    def objects_right(self, player):
        return [
            obj
            for obj in self.all_objects()
            if obj.is_to_the_right(player.image.shape)
        ]

    def walls_under(self, player):
        """
        All the walls currently positioned under the player
        """
        ans = [
            wall
            for wall in self.walls
            if wall.is_under(player.image.shape)]
        return ans

    def walls_right(self, player):
        """
        All the walls the player collides with to his right hand side
        """
        ans = [
            wall
            for wall in self.walls
            if wall.is_to_the_right(player.image.shape)]  # the player's right border is the wall's left -> check wall's left collision
        return ans


    def walls_left(self, player):
        """
        All the walls the player collides with to his left hand side
        """
        ans = [
            wall
            for wall in self.walls
            if wall.is_to_the_left(player.image.shape)]  # see `walls_right`
        return ans

    def limit_under(self, player):
        distances = [
            player.image.shape.distance_y(wall.image.shape) - 1
            for wall in self.walls_under(player)]
        
        return min(distances + [self.MAX_POSITION])

    def limit_right(self, player):
        distances = [
            player.image.shape.distance_x(wall.image.shape) - 1
            for wall in self.walls_right(player)]

        return min(distances + [self.MAX_POSITION])

    def limit_left(self, player):
        distances = [
            player.image.shape.distance_x(wall.image.shape) + 1
            for wall in self.walls_left(player)]

        return max(distances + [self.MIN_POSITION])


    # returns true if player is colliding with the nearest wall on their right hand side
    def is_colliding_wall_right(self, player):
        return player.image.shape.right == self.limit_right(player)

    def is_colliding_wall_left(self, player):
        return player.image.shape.left == self.limit_left(player)

    def remove(self, game_object):
        obj_type = type(game_object)
        known_objects_of_type = self.of_type(obj_type)
        known_objects_of_type.remove(game_object)
