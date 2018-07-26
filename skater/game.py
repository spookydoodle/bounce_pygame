from .state import *
from .player import *
from .gameboard import *
from .obstacles import *
from .score import *


class Game(State):

    def __init__(self):
        State.__init__(self)
        self.active_state = "game"
        self.level = 0

        self.game_board = GameBoard([])

        self.player = Player(speed = 4)
        self.player.rect.x = 100
        self.player.rect.bottom = 500
        
        self.score = Score(3)

        self.game_over = False
        self.won_level = False
        self.new_level = True

        self.CameraX = 0


    def process_events(self):
        if self.active_state == "Menu": return Menu()
        else: return self

    
    def run(self, screen, event):
        
        if self.new_level:
            self.level += 1
            self.game_board.obstacles = self.create_obstacles()
            self.player.rect.x = 100
            self.player.rect.bottom = 700
            self.new_level = False

        if not self.game_over:
            if not self.won_level:
                
                if self.player.rect.x > screen.get_rect().midtop[0]:
                    self.CameraX += 0

                elif self.player.rect.x < (screen.get_rect().x + 0.2 * screen.get_rect().width):
                    self.CameraX -= 0

                else: 
                    self.CameraX = 0

                self.check_collisions()
                self.player.move(screen, event, self.CameraX)

                # The player cannot fall lower than the highest of obstacles under him
                falling_limit = min(obstacle.rect.top for obstacle in self.obstacles_under())
                self.player.move_y(falling_limit)
                self.change_obstacles_pos_cam()
                self.check_game_result()

            # You won level screen - press any key to move to next level
            else: 
                self.won_level_continue(event)

        # Game over screen action - press any key and move to menu
        else:
            self.game_over_continue(event)
    
    # this is still working/testing version of this function...
    def create_obstacles(self):

        ground = Obstacle(image = pygame.Surface([2000, 50]), x = 0, y = 700)

        obstacle2 = Obstacle(image = pygame.Surface([400, 25]), x = 500, y = 675)

        obstacle3 = Obstacle(image = pygame.Surface([50, 700]), x = 0, y = 0)

        obstacle4 = Obstacle(image = pygame.Surface([50, 700]), x = 1950, y = 0)

        obstacles = [ground, obstacle2, obstacle3, obstacle4]
        
        return obstacles
               

    def obstacles_under(self):
        """
        All the obstacles currently positioned under the player
        """
        ans = [
            obstacle
            for obstacle in self.game_board.obstacles
            if obstacle.is_under(self.player.rect)]
        return ans


    def change_obstacles_pos_cam(self):
        for sprite in self.game_board.obstacles: sprite.rect.x -= self.CameraX


    def check_collisions(self):
        var1 = (self.player.is_colliding_r, self.player.is_colliding_l, self.player.is_colliding_b, self.player.rect.bottom)
        # reset collision flags
        self.player.is_colliding_l = False
        self.player.is_colliding_r = False
        self.player.is_colliding_t = False
        self.player.is_colliding_b = False

        # set collision flags if player collides with an obstacle
        collision_list = pygame.sprite.spritecollide(self.player, self.game_board.obstacles, False)
        
        for obstacle in collision_list:
            
            self.check_collision_r(obstacle)
            self.check_collision_l(obstacle)
            #self.check_collision_t(obstacle)
            self.check_collision_b(obstacle)


    # check collision player_right - obstacle_left
    def check_collision_r(self, obstacle):

        if pygame.sprite.collide_rect(self.player, obstacle) \
            and self.player.rect.left <= obstacle.rect.left \
            and self.player.rect.right >= obstacle.rect.left \
            and self.player.rect.bottom > obstacle.rect.top:

            self.player.stop_movement_x()
            self.player.is_colliding_r = True


    # check collision player_left - obstacle_right
    def check_collision_l(self, obstacle):

        if pygame.sprite.collide_rect(self.player, obstacle) \
            and self.player.rect.left <= obstacle.rect.right \
            and self.player.rect.right >= obstacle.rect.right \
            and self.player.rect.bottom > obstacle.rect.top:

            self.player.stop_movement_x()
            self.player.is_colliding_l = True


    # check collision player_bottom - obstacle_top - not working yet
    def check_collision_b(self, obstacle):

        ## this condition is added to avoid changing y position when player collides with a corner of an obstacle (e.g., top left point)
        #if not self.player.is_colliding_r and not self.player.is_colliding_l:

        # additional conditions are given to handle situations where collision appears on the corners of an obstacle
        if pygame.sprite.collide_rect(self.player, obstacle) \
            and self.player.rect.bottom >= obstacle.rect.top \
            and self.player.rect.top <= obstacle.rect.top \
            \
            and self.player.rect.right > obstacle.rect.left \
            and self.player.rect.left > (obstacle.rect.left - self.player.rect.width) \
                \
            and self.player.rect.right < (obstacle.rect.right + self.player.rect.width) \
            and self.player.rect.left < obstacle.rect.right:
            
            self.player.stop_movement_y(obstacle.rect.top)
            self.player.is_colliding_b = True 


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
        screen.fill(WHITE, (0 - self.CameraX, 0, screen.get_size()[0], screen.get_size()[1]))

        if not self.game_over:

            # main game
            if not self.won_level:
                self.draw_main_game(screen, BLACK)

            # you won level screen
            else:
                # self.level - 1 because drawing takes place in main after score was increased
                won_level_text = ["Level " + str(self.level) + " beated!", "Press Y key to continue"]
                for i, text in enumerate(won_level_text):
                    draw_text(screen, text, font, BLACK, "L", 500 - self.CameraX, 300 + i * 50)

        # Game over screen
        else:
            game_over_text = ["You lost!", "Total score: {}".format(self.score.total_score),  "Do you want to continue? Y/N"]
            for i, text in enumerate(game_over_text):
                draw_text(screen, text, font, BLACK, "L", 500 - self.CameraX, 300 + i * 50)

            self.draw_main_game(screen, BLACK)

        pygame.display.update()

    
    def draw_main_game(self, screen, color):

        ## draw ground
        #self.draw_ground(screen, color)

        # draw sprites (player and obstacles)
        draw_sprite(screen, self.player)
        for sprite in self.game_board.obstacles:
            draw_sprite(screen, sprite) 

        # Draw scores in right top corner
        self.draw_game_results(screen, self.score, color)

        # update player image in new position
        screen.blit(self.player.image, (self.player.rect.x - self.CameraX, self.player.rect.y))


    ##def draw_keyword(self, screen, kw_list, color):
    ##    font = pygame.font.SysFont('Arial', 45)
    ##    a = 30; b = 0
    ##    for word in kw_list:
    ##        word = word + " "
    ##        if len(word) > a: a = 30; b +=1
    ##        for c in word:
    ##            draw_text(screen, c, font, color, "L", (550 + (30-a)*35), (100 + b*60))
    ##            a -= 1    

    def draw_ground(self, screen, color):
        screen.fill(color, (0, 700, screen.get_size()[0], 20))


    def draw_game_results(self, screen, score, color):
        font = pygame.font.SysFont('Arial', 20)
        game_results_list = ["Level: {}".format(self.level),
                             "Lives: {}".format(str(score.number_of_lives)),
                             "Score: {}".format(str(score.total_score))]
        
        for n, result in enumerate(game_results_list):
            draw_text(screen, result, font, color, "R", screen.get_rect().width - 10, (10 + n*30))
