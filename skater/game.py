from .state import *
from .player import *
from .gameboard import *
from .obstacles import *
from .obstacles_list import *
from .score import *
from .camera import *
from skater.destination import Destination
from . import image, image_paths

class Game(State):

    def __init__(self):
        State.__init__(self)
        self.active_state = "game"
        self.level = 0

        self.gameboard = GameBoard([])

        self.player = Player(speed_unit = 8)
        self.player.rect.x = 100
        self.player.rect.bottom = 500
        
        self.score = Score(3)

        self.game_over = False
        self.won_level = False
        self.new_level = True

        self.camera = Camera()


    def next_destination(self):
        if self.active_state == "Menu": return Desination.MENU
        elif self.active_state == "Exit": return Destination.EXIT

    
    def run(self, screen, event):
        if event.type == pygame.KEYDOWN and event.key in CONTROLS["QUIT"]:
            self.active_state = "Exit"
        
        if self.new_level:
            self.level += 1
            self.gameboard.obstacles = self.create_obstacles()
            self.player.rect.x = 100
            self.player.rect.bottom = 500
            self.new_level = False

        if not self.game_over:
            if not self.won_level:

                # changes x and y parameters of camera depending on the location of the player on the screen
                self.camera.adjust(screen, self.player)

                self.player.move(screen, event, self.gameboard)
                self.check_game_result()

            # You won level screen - press any key to move to next level
            else: 
                self.won_level_continue(event)

        # Game over screen action - press any key and move to menu
        else:
            self.game_over_continue(event)
    
    # return all obstacle objects listed in OBSTACLES in obstacles_list.py
    def create_obstacles(self):
        return [
            Obstacle(
                image = image.Image.create(obstacle[1]),
                x = obstacle[0][0],
                y = obstacle[0][1])
            for obstacle in list(OBSTACLES.values())]


    def check_game_result(self):
        if self.player.is_crashed():
            self.game_over = True

    
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
        WHITE = (255, 255, 255)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        
        font = pygame.font.SysFont('Arial', 40)

        # clean game area
        screen.fill(WHITE, (0, 0, screen.get_size()[0], screen.get_size()[1]))

        if not self.game_over:

            # main game
            if not self.won_level:
                self.draw_main_game(screen, BLACK)

            # you won level screen
            else:
                # self.level - 1 because drawing takes place in main after score was increased
                won_level_text = ["Level " + str(self.level) + " beated!", "Press Y key to continue"]
                for i, text in enumerate(won_level_text):
                    draw_text(screen, text, font, BLACK, "L", 500, 300 + i * 50)

        # Game over screen
        else:
            game_over_text = ["You lost!", "Total score: {}".format(self.score.total_score),  "Do you want to continue? Y/N"]
            for i, text in enumerate(game_over_text):
                draw_text(screen, text, font, BLACK, "L", 500, 300 + i * 50)

            self.draw_main_game(screen, BLACK)

        pygame.display.update()

    
    def draw_main_game(self, screen, color):

        # draw sprites (player and obstacles)
        draw_sprite(screen, self.player, self.camera)

        for sprite in self.gameboard.obstacles:
            draw_sprite(screen, sprite, self.camera) 

        # Draw scores in right top corner
        self.draw_game_results(screen, self.score, color)
  

    def draw_ground(self, screen, color):
        screen.fill(color, (0, 700, screen.get_size()[0], 20))


    def draw_game_results(self, screen, score, color):
        font = pygame.font.SysFont('Arial', 20)
        game_results_list = ["Level: {}".format(self.level),
                             "Lives: {}".format(str(score.number_of_lives)),
                             "Score: {}".format(str(score.total_score))]
        
        for n, result in enumerate(game_results_list):
            draw_text(screen, result, font, color, "R", screen.get_rect().width - 10, (10 + n*30))


