import pygame
from pygame.locals import *
from .dicts import *


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, image_path = None, image = None, x = 0, y = 0):
        super().__init__()

        if image_path != None:
            self.image = pygame.image.load(image_path).convert_alpha()
        else: 
            self.image = image
            self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    # this is still working/testing version of this function...
    def create_obstacles(self):
        
        self.all_sprites_group = pygame.sprite.Group()
        self.all_sprites = []

        ground = Obstacle(image = pygame.Surface([2000, 50]), x = 0, y = 700)

        obstacle2 = Obstacle(image = pygame.Surface([400, 25]), x = 500, y = 675)

        obstacle3 = Obstacle(image = pygame.Surface([50, 700]), x = 0, y = 0)

        obstacle4 = Obstacle(image = pygame.Surface([50, 700]), x = 1950, y = 0)

        obstacles = [ground, obstacle2, obstacle3, obstacle4]
        
        for obstacle in obstacles:
            self.all_sprites.append(obstacle)
            self.all_sprites_group.add(obstacle)

        self.obstacles = obstacles
               

    def obstacles_under(self):
        """
        All the obstacles currently positioned under the player
        """
        ans = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.is_under(self.player.rect)]
        return ans


    def obstacles_right(self):
        """
        All the obstacles currently positioned on the right to the player
        """
        ans = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.is_colliding_right(self.player.rect)]
        return ans


    def obstacles_left(self):
        """
        All the obstacles currently positioned on the left of the player
        """
        ans = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.is_colliding_left(self.player.rect)]
        return ans


    def change_obstacles_pos_cam(self):
        for sprite in self.all_sprites: sprite.rect.x -= self.CameraX


    # collision player bottom - obstacle top
    def is_under(self, other_rect):
        return self.rect.bottom > other_rect.bottom and self.rect.left < other_rect.right and self.rect.right > other_rect.left


    # collision player top - obstacle bottom
    def is_over(self, other_rect):
        return self.rect.top < other_rect.top and self.rect.left < other_rect.right and self.rect.right > other_rect.left


    # collision player right - obstacle left
    def is_colliding_right(self, other_rect):
        return self.rect.left >= other_rect.left and self.rect.left <= other_rect.right and self.rect.top < oother_rect.bottom

    
    # collision player left - obstacle right
    def is_colliding_left(self, other_rect):
        return self.rect.right >= other_rect.left and self.rect.right <= other_rect.right and self.rect.top < oother_rect.bottom
