
class GameBoard:
    # infinities to avoid crashes on empty sequence computations
    MIN_POSITION = -2 ** 31
    MAX_POSITION = 2 ** 31

    def __init__(self, walls, collectables, obstacles, bullets):
        self.walls = walls
        self.collectables = collectables
        self.obstacles = obstacles
        self.bullets = bullets

    def walls_under(self, player):
        """
        All the walls currently positioned under the player
        """
        ans = [
            wall
            for wall in self.walls
            if wall.is_under(player.rect)]
        return ans


    def walls_right(self, player):
        """
        All the walls the player collides with to his right hand side
        """
        ans = [
            wall
            for wall in self.walls
            if wall.is_to_the_right(player.rect)]  # the player's right border is the wall's left -> check wall's left collision
        return ans


    def walls_left(self, player):
        """
        All the walls the player collides with to his left hand side
        """
        ans = [
            wall
            for wall in self.walls
            if wall.is_to_the_left(player.rect)]  # see `walls_right`
        return ans

    def limit_under(self, player):
        distances = [
            player.rect.distance_y(wall.rect) - 1
            for wall in self.walls_under(player)]
        
        return min(distances + [self.MAX_POSITION])

    def limit_right(self, player):
        distances = [
            player.rect.distance_x(wall.rect) - 1
            for wall in self.walls_right(player)]

        return min(distances + [self.MAX_POSITION])

    def limit_left(self, player):
        distances = [
            player.rect.distance_x(wall.rect) + 1
            for wall in self.walls_left(player)]

        return max(distances + [self.MIN_POSITION])


    # returns true if player is colliding with the nearest wall on their right hand side
    def is_colliding_wall_right(self, player):
        return player.rect.right == self.limit_right(player)

    def is_colliding_wall_left(self, player):
        return player.rect.left == self.limit_left(player)