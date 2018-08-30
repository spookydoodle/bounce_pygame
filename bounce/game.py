from .state import *
from .player import *
from .gameboard import *
from .game_object import *
from .game_objects_init_list import *
from .score import *
from .camera import *
from .destination import Destination
from . import image, image_paths
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Game(State):

    def __init__(self):
        State.__init__(self)
        self.active_state = "Play"
        self.level = 0

        self.gameboard = GameBoard([], [])

        self.player = Player(speed_unit = 8)
        self.player.rect.x = 200
        self.player.rect.bottom = -100
        
        self.score = Score(3)

        self.won_level = False
        self.new_level = True

        self.camera = Camera()


    def next_destination(self):
        if self.active_state == "Menu": return Destination.MENU
        elif self.active_state == "Exit": return Destination.EXIT

    
    def run(self, screen, event):
        if event.type == pygame.KEYDOWN and event.key in CONTROLS["QUIT"]:
            self.active_state = "Exit"
        
        if self.new_level:
            self.level += 1
            self.gameboard.walls = self.create_init_walls()
            self.gameboard.collectables = self.create_init_collectables()
            self.player.rect.x = 200
            self.player.rect.bottom = -100
            self.new_level = False

        if not self.is_game_over():
            if not self.won_level:

                # append new walls and delete invisible ones depending on player.y position
                self.edit_walls_list(screen)
                self.edit_collectables_list(screen)
                
                # changes x and y parameters of camera depending on the location of the player on the screen
                self.camera.adjust(screen, self.player)

                self.player.move(screen, event, self.gameboard)
                #self.check_game_result()

            # You won level screen - press any key to move to next level
            else: 
                self.won_level_continue(event)

        # Game over screen action - press any key and move to menu
        else:
            self.game_over_continue(event)
    
    # return all wall objects listed in WALLS in walls_list.py
    def create_init_walls(self):
        return [
            GameObject(
                image = image.Image.create( (wall['size']['width'], wall['size']['height']), color = BLUE ),
                x = wall['position']['x'],
                y = wall['position']['y'])
            for wall in list(GAME_OBJECTS.values()) if wall['type'] == 1]  


    def edit_walls_list(self, screen):
        self.check_append_wall(screen)
        self.check_remove_wall(screen)


    def append_wall(self):

        width = 50
        x_positions = [100, 300, 500]

        for x_pos in x_positions:

            height = random.randint(100, 400)
            distance = random.randint(75, 150)

            self.gameboard.walls.append( GameObject(
                image = image.Image.create( (width, height), color = BLUE ), 
                x = x_pos,
                y = self.gameboard.walls[-len(x_positions)].rect.y - distance - height)
                )

    def remove_wall(self, n = 0):
        del self.gameboard.walls[n]


    def check_append_wall(self, screen):
        if abs(self.gameboard.walls[-1].rect.y - self.player.rect.y) < pygame.display.get_surface().get_rect().height:
            self.append_wall()

    
    def check_remove_wall(self, screen):
        if abs(self.gameboard.walls[0].rect.y - self.player.rect.y) > pygame.display.get_surface().get_rect().height:
            self.remove_wall()


    def create_init_collectables(self):
        return [
            GameObject(
                image = image.Image.create( (collectable['size']['width'], collectable['size']['height']), color = GREEN ),
                x = collectable['position']['x'],
                y = collectable['position']['y'])
            for collectable in list(GAME_OBJECTS.values()) if collectable['type'] == 2]  


    def edit_collectables_list(self, screen):
        self.check_append_collectable(screen)
        self.check_remove_collectable(screen)
            
    def append_collectable(self):

        width = 50
        x_positions = [random.randint(150, 250), random.randint(350, 450)]

        self.gameboard.collectables.append( GameObject(
            image = image.Image.create( (50, 50), color = GREEN ), 
            x = x_positions[random.randint(0, 1)],
            y = self.gameboard.collectables[-1].rect.y - random.randint(0,500))
            )

    def remove_collectable(self, n = 0):
        del self.gameboard.collectables[n]
    

    def check_append_collectable(self, screen):
        if abs(self.gameboard.collectables[-1].rect.y - self.player.rect.y) < pygame.display.get_surface().get_rect().height:
            self.append_collectable()
    

    def check_remove_collectable(self, screen):
        if abs(self.gameboard.collectables[0].rect.y - self.player.rect.y) > pygame.display.get_surface().get_rect().height:
            self.remove_collectable()

    def is_game_over(self):
        return self.player.is_crashed()

    
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
               
        font = pygame.font.SysFont('Arial', 40)

        # clean game area
        screen.fill(BLACK, (0, 0, screen.get_size()[0], screen.get_size()[1]))

        if not self.is_game_over():

            # main game
            if not self.won_level:
                self.draw_main_game(screen)
                self.draw_game_results(screen, self.score, WHITE)

            # you won level screen
            else:
                self.draw_won_level_screen(screen, font, WHITE)

        # Game over screen
        else:
            self.draw_main_game(screen)
            self.draw_game_over_screen(screen, font, WHITE)


        pygame.display.update()

    
    def draw_main_game(self, screen):

        # draw sprites (player and walls)
        draw_rect(screen, self.camera, self.player.rect, self.player.image)

        for sprite in self.gameboard.walls:
            draw_rect(screen, self.camera, sprite.rect, sprite.image)

        for sprite in self.gameboard.collectables:
            draw_rect(screen, self.camera, sprite.rect, sprite.image) 
  
    
    def draw_won_level_screen(self, screen, font, color):
        won_level_text = ["Level " + str(self.level) + " beated!", "Press Y key to continue"]

        for i, text in enumerate(won_level_text):
            draw_text(screen, text, font, color, "L", 500, 300 + i * 50)


    def draw_game_over_screen(self, screen, font, color):
        game_over_text = ["You lost!", "Total score: {}".format(self.score.total_score),  "Do you want to continue? Y/N"]

        for i, text in enumerate(game_over_text):
            draw_text(screen, text, font, color, "L", 100, 300 + i * 50)


    def draw_ground(self, screen, color):
        screen.fill(color, (0, 700, screen.get_size()[0], 20))


    def draw_game_results(self, screen, score, color):
        font = pygame.font.SysFont('Arial', 20)
        game_results_list = ["Level: {}".format(self.level),
                             "Lives: {}".format(str(score.number_of_lives)),
                             "Score: {}".format(str(score.total_score))]
        
        for n, result in enumerate(game_results_list):
            draw_text(screen, result, font, color, "R", screen.get_rect().width - 10, (10 + n*30))


