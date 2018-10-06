from silnik.image import Image
from silnik.rendering.shape import Polygon, rectangle
from silnik.rendering.point import Point
from silnik.rendering.text import Text

from .collectable import Collectable
from .obstacle import Obstacle
from .wall import Wall
from .state import *
from .player import *
from .gameboard import *
from .game_object import *
from .game_objects_init_list import *
from .score import *
from .camera import *
from .destination import Destination
from .constants import *
from . import image_paths

import random



class Game(State):

    def __init__(self):
        State.__init__(self)
        self.active_state = "Play"
        self.level = 0
        self.score = Score(3)

        self.gameboard = GameBoard(walls = [], 
                                   collectables = [], 
                                   obstacles = [], 
                                   bullets = [])

        # Build a player instance, inject `on_*_collision` handlers to keep track of the score
        self.player = Player(
            speed_unit = 8,
            on_obstacle_collision=lambda: self.score.decrease_lives(),
            on_collectable_collision=lambda: self.score.add_points()
        )

        self.won_level = False
        self.new_level = True
        
        # Make the camera focus on the point above the player.
        # Effectively renders the player on the bottom of the screen.
        camera_focus_shift = Point(0, -300)
        self.camera = Camera(camera_focus_shift)


    def next_destination(self):
        if self.active_state == "Menu": return Destination.MENU
        elif self.active_state == "Exit": return Destination.EXIT
    
    def run(self, screen, event):
        if event.type == pygame.KEYDOWN and event.key in CONTROLS["QUIT"]:
            self.active_state = "Exit"
        
        if self.new_level:
            self.init_new_level()

        if not self.is_game_over():
            if not self.won_level:

                # append new walls and delete invisible ones depending on player.y position
                self.edit_game_objects(screen)
                print("W", len(self.gameboard.walls),
                      "C",  len(self.gameboard.collectables),
                      "O", len(self.gameboard.obstacles),
                      "B",  len(self.gameboard.bullets),)
                print(self.last_wall_y, self.last_collectable_y, self.last_obstacle_y, self.player.image.shape.y)
                
                # changes x and y parameters of camera depending on the location of the player on the screen
                self.camera.adjust(screen, self.player)

                # update player and its bullets positions
                self.player.process_event(event)
                self.player.move(self.gameboard)
                self.player.append_bullet(event, self.gameboard)

                self.move_bullets()
                self.score.update_meters(-self.player.image.shape.y)

                self.check_won()

            # You won level screen - press any key to move to next level
            else: 
                self.won_level_continue(event)

        # Game over screen action - press any key and move to menu
        else:
            self.game_over_continue(event)

    def init_new_level(self):
        self.level += 1
        self.score.reset()
        self.camera.reset()
        self.gameboard.walls = self.create_init_walls()
        self.gameboard.collectables = self.create_init_collectables()
        self.gameboard.obstacles = self.create_init_obstacles()
        self.gameboard.bullets = []
        self.player.image.shape.x = 200
        self.player.image.shape.bottom = -100
        self.last_wall_y = -390
        self.last_collectable_y = -1000
        self.last_obstacle_y = -400
        self.new_level = False

    @staticmethod
    def dict_data_to_arguments(data):
        x = data['position']['x']
        y = data['position']['y']
        width = data['size']['width']
        height = data['size']['height']
        size = (width, height)
        return (size, x, y)

    # return all wall objects listed in WALLS in walls_list.py
    def create_init_walls(self):
        return [
            Wall.build(*self.dict_data_to_arguments(data))
            for data in list(GAME_OBJECTS.values()) if data['type'] == 1]

    def create_init_collectables(self):
        return [
            Collectable.build(*self.dict_data_to_arguments(data))
            for data in list(GAME_OBJECTS.values()) if data['type'] == 2]

    def create_init_obstacles(self):
        return [
            Obstacle.build(*self.dict_data_to_arguments(data))
            for data in list(GAME_OBJECTS.values()) if data['type'] == 3]

    def game_object_lists(self):

        return [self.gameboard.walls, 
                self.gameboard.collectables, 
                self.gameboard.obstacles,
                self.gameboard.bullets]

    def last_game_object_y(self, game_object_list):

        if game_object_list == self.gameboard.walls: return self.last_wall_y
        if game_object_list == self.gameboard.collectables: return self.last_collectable_y
        if game_object_list == self.gameboard.obstacles: return self.last_obstacle_y


    def edit_game_objects(self, screen):

        for game_object_list in self.game_object_lists():

            self.check_append_game_objects(screen, game_object_list, self.last_game_object_y(game_object_list))
            self.check_remove_game_object(screen, game_object_list)


    def append_wall(self):

        width = 50
        x_positions = [100, 300, 500]
        
        for x_pos in x_positions:
            self.last_wall_y = self.gameboard.walls[-len(x_positions)].image.shape.y
            height = random.randint(100, 400)
            distance = random.randint(75, 150)

            self.gameboard.walls.append(
                Wall.build(
                    (width, height),
                    x_pos,
                    y = self.last_wall_y - distance - height))
            
    def append_collectable(self):
        width = 50
        x_positions = [random.randint(150, 250), random.randint(350, 450)]
        self.last_collectable_y -= random.randint(0,500)

        self.gameboard.collectables.append(
            Collectable.build(
                (50, 50),
                x_positions[random.randint(0, (len(x_positions)-1))],
                y = self.last_collectable_y))
            
    def append_obstacle(self):

        width = 50
        x_positions = [150, 250, 350, 450]
        self.last_obstacle_y -= random.randint(200,500)

        self.gameboard.obstacles.append(
            Obstacle.build(
                (50, 50),
                x_positions[random.randint(0, (len(x_positions)-1))],
                self.last_obstacle_y))

    def append_game_objects(self):
        self.append_wall()
        self.append_collectable()
        self.append_obstacle()

    def check_append_game_objects(self, screen, game_object_list, last_y):
        if game_object_list != self.gameboard.bullets:
            if abs(last_y - self.player.image.shape.y) < pygame.display.get_surface().get_rect().height:
                self.append_game_objects()

    
    def check_remove_game_object(self, screen, game_object_list):
        #if game_object_list != self.gameboard.bullets or (game_object_list == self.gameboard.bullets and len(game_object_list) > 0):
        if len(game_object_list) > 0:
            first_object = game_object_list[0]
            if abs(first_object.image.shape.y - self.player.image.shape.y) > pygame.display.get_surface().get_rect().height:
                self.gameboard.remove(first_object)

    def check_won(self):
        if self.score.points >= 50:
            self.won_level = True

    def move_bullets(self):
        for bullet in self.gameboard.bullets:
            bullet.move(self.gameboard)


    # TODO : player.is_crashed should be true also if player collides with an obstacle
    # TODO: is_game_over needs to be rewritten to make a bit more sense
    def is_game_over(self):
        return self.player.is_crashed() or self.score.number_of_lives == 0

    def game_over_continue(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in CONTROLS["YES"]:
                self.active_state = "Menu"
            elif event.key == pygame.K_n:
                self.exit = True


    def won_level_continue(self, event):
        if event.type == pygame.KEYDOWN and event.key in CONTROLS["YES"]: 
            self.won_level = False
            self.new_level = True


    def display_frame(self, screen, background_image):

        # clean game area
        screen.fill(Colors.BLACK, (0, 0, screen.get_size()[0], screen.get_size()[1]))

        if not self.is_game_over():

            # main game
            if not self.won_level:
                self.draw_main_game(screen)
                self.draw_game_results(screen, self.score, Colors.WHITE)

            # you won level screen
            else:
                self.draw_won_level_screen(screen)

        # Game over screen
        else:
            self.draw_main_game(screen)
            self.draw_game_over_screen(screen)


        pygame.display.update()

    
    def draw_main_game(self, screen):

        for game_object_list in self.game_object_lists():
            for sprite in game_object_list:
                sprite.image.render(screen, self.camera)
                
        # draw player
        self.player.image.render(screen, self.camera)

    def renderable_text(self, text, x, y, x_anchor="left", y_anchor="top"):
        """
        A helper to draw a text relative to the screen.

        If x_anchor == "right", the text will be drawn relative to the right edge.
        If x_anchor == "bottom", the text will be drawn relative to the bottom edge.
        """
        renderable_text = Image.from_pyimage(text.pre_render())
        
        if x_anchor == "left":
            renderable_text.shape.left = x
        elif x_anchor == "right":
            renderable_text.shape.right = x
        
        if y_anchor=="top":
            renderable_text.shape.top = y
        elif y_anchor=="bottom":
            renderable_text.shape.bottom = y

        return renderable_text

    def draw_game_results(self, screen, score, color):
        game_results_list = ["Level: {}".format(self.level),
                             "Lives: {}".format(str(score.number_of_lives)),
                             "Meters: {}".format(str(score.meters)),
                             "Points: {}".format(str(score.points))]
        
        x_position = screen.get_rect().width - 10
        
        for n, result in enumerate(game_results_list):
            text = Text(str(result), font_size=20, font_color=Colors.MAGENTA)
            self.renderable_text(text, x_position, 10 + n * 30, x_anchor="right").render(screen)

    def draw_won_level_screen(self, screen):
        won_level_text = ["Level " + str(self.level) + " beaten!", "Press Y key to continue"]

        for i, line in enumerate(won_level_text):
            text = Text(line, font_size=20, font_color=Colors.WHITE)
            self.renderable_text(text, 100, 300 + i * 50).render(screen)


    def draw_game_over_screen(self, screen):
        game_over_text = ["You lost!", 
                          "Points collected: {}!".format(self.score.points), 
                          "You went up {} meters!".format(self.score.meters),
                          "",
                          "Do you want to continue? Y/N"]

        for i, line in enumerate(game_over_text):
            text = Text(line, font_size=20, font_color=Colors.WHITE)
            self.renderable_text(text, 100, 250 + i * 50).render(screen)