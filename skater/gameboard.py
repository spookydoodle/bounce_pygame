
class GameBoard:

    def __init__(self, obstacles):
        self.obstacles = obstacles


    #def change_obstacles_pos_cam(self):
    #    for obstacle in self.obstacles: obstacle.rect.x -= self.CameraX


    def obstacles_under(self, player):
        """
        All the obstacles currently positioned under the player
        """
        ans = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.is_under(player.rect)]
        return ans


    def obstacles_right(self, player):
        """
        All the obstacles the player collides with to his right hand side
        """
        ans = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.is_colliding_left(player.rect)]  # the player's right border is the obstacle's left -> check obstacle's left collision
        return ans


    def obstacles_left(self, player):
        """
        All the obstacles the player collides with to his left hand side
        """
        ans = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.is_colliding_right(player.rect)]  # see `obstacles_right`
        return ans