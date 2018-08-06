from .state import *
from .player import *
from .gameboard import *
from .obstacles import *
from .score import *
from .camera import *
from skater.destination import Destination


class Game(State):

    def __init__(self):
        State.__init__(self)
        self.active_state = "game"
        self.level = 0

        self.gameboard = GameBoard([])

        self.player = Player(speed = 4)
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
                # The player cannot fall lower than the highest of obstacles under him
                self.player.move_y(self.gameboard)
                self.check_game_result()

            # You won level screen - press any key to move to next level
            else: 
                self.won_level_continue(event)

        # Game over screen action - press any key and move to menu
        else:
            self.game_over_continue(event)
    
    # this is still working/testing version of this function...
    def create_obstacles(self):

        ground = Obstacle(image = pygame.Surface([1200, 50]), x = 0, y = 600)

        ground2 = Obstacle(image = pygame.Surface([800, 50]), x = 1200, y = 700)

        obstacle2 = Obstacle(image = pygame.Surface([300, 25]), x = 500, y = 575)

        obstacle3 = Obstacle(image = pygame.Surface([50, 400]), x = 0, y = 200)

        obstacle4 = Obstacle(image = pygame.Surface([50, 400]), x = 1950, y = 350)

        obstacles = [ground, ground2, obstacle2, obstacle3, obstacle4]
        
        return obstacles


    def check_game_result(self):
        if self.player.is_crash:
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
        screen.fill(WHITE, (0 - self.camera.x, 0, screen.get_size()[0], screen.get_size()[1]))

        if not self.game_over:

            # main game
            if not self.won_level:
                self.draw_main_game(screen, BLACK)

            # you won level screen
            else:
                # self.level - 1 because drawing takes place in main after score was increased
                won_level_text = ["Level " + str(self.level) + " beated!", "Press Y key to continue"]
                for i, text in enumerate(won_level_text):
                    draw_text(screen, text, font, BLACK, "L", 500 - self.camera.x, 300 + i * 50)

        # Game over screen
        else:
            game_over_text = ["You lost!", "Total score: {}".format(self.score.total_score),  "Do you want to continue? Y/N"]
            for i, text in enumerate(game_over_text):
                draw_text(screen, text, font, BLACK, "L", 500 - self.camera.x, 300 + i * 50)

            self.draw_main_game(screen, BLACK)

        pygame.display.update()

    
    def draw_main_game(self, screen, color):

        # draw sprites (player and obstacles)
        draw_sprite(screen, self.player, self.camera)

        for sprite in self.gameboard.obstacles:
            draw_sprite(screen, sprite, self.camera) 

        # Draw scores in right top corner
        self.draw_game_results(screen, self.score, color)

        # update player image in new position
        screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
  

    def draw_ground(self, screen, color):
        screen.fill(color, (0, 700, screen.get_size()[0], 20))


    def draw_game_results(self, screen, score, color):
        font = pygame.font.SysFont('Arial', 20)
        game_results_list = ["Level: {}".format(self.level),
                             "Lives: {}".format(str(score.number_of_lives)),
                             "Score: {}".format(str(score.total_score))]
        
        for n, result in enumerate(game_results_list):
            draw_text(screen, result, font, color, "R", screen.get_rect().width - 10, (10 + n*30))


