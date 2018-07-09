import pygame
from pygame.locals import *
from .player import *
from .obstacles import *
from .score import *
from .dicts import *


class State:
    
    def __init__(self):
        self.active_state = ""
        self.exit = False

    def process_events(self):
        raise NotImplementedError
    
    def run(self):
        raise NotImplementedError
    
    def display_frame(self, background_image):
        raise NotImplementedError

    def check_exit(self):
        if self.exit: return True
        else: return False


class Menu(State):
    
    OPTIONS = ["Play", 
               "Controls", 
               "Exit"]

    def __init__(self):
        State.__init__(self)
        self.active_state = "Menu"
        self.selected_index = 0


    def _next_index(self):
        max = len(self.OPTIONS)
        return (self.selected_index + 1) % max


    def _previous_index(self):
        max = len(self.OPTIONS)
        return (self.selected_index - 1) % max


    def process_events(self):

            if self.active_state == "Play": return Game()
            elif self.active_state == "Controls" : return Controls()
            elif self.active_state in ("Menu", "Next_Level"): return self
            #elif self.active_state == "Exit": return self; self.exit = True
            elif self.active_state == "Exit": pygame.quit()

    
    def run(self, screen, event): 
        
        if event.type == pygame.KEYDOWN:

            if event.key in CONTROLS["M_DOWN"] and self.selected_index < (len(self.OPTIONS) - 1):
                self.selected_index = self._next_index()

            if event.key in CONTROLS["M_UP"] and self.selected_index > 0:
                self.selected_index = self._previous_index()

            if event.key in CONTROLS["M_SELECT"]:
               #if self.selected_index == 0: self.active_state = "game"
               #if self.selected_index == 1: self.active_state = "controls"
               #if self.selected_index == 2: pygame.quit()
               self.active_state = self.OPTIONS[self.selected_index]


    def display_frame(self, screen, background_image):
        font = pygame.font.SysFont('Arial', 60)
        BLACK = (0, 0, 0); WHITE = (255, 255, 255); RED = (255, 0, 0)
        selected_marker = ">"; unselected_marker = " "

        # clean game area
        screen.blit(background_image, (0, 0))

        for i in range(len(self.OPTIONS)):
            if i == self.selected_index: text = "{} {}".format(selected_marker, self.OPTIONS[i])
            else: text = "{} {}".format(unselected_marker, self.OPTIONS[i])

            draw_text(screen, text, font, BLACK, "L", 550, 250 + i*100)

        pygame.display.update()


class Controls(State):
    
    # dictionary with assignment and descriptions of control keys
    CONTROLS_DESC = [["Right", "D / Right Arrow"],
                ["Left", "A / Left Arrow"],
                ["Jump / Ollie", "Space"],
                ["Manual / Grind", "W / Up Arrow"],
                ["Back", "B / Return"]
                ]


    def __init__(self):
        State.__init__(self)
        self.active_state = "Controls"
        self.selected_index = 4


    def _next_index(self):
        max = len(self.CONTROLS_DESC)
        return (self.selected_index + 1) % max


    def _previous_index(self):
        max = len(self.CONTROLS_DESC)
        return (self.selected_index - 1) % max


    def process_events(self):

            if self.active_state == "Back": return Menu()
            else: return self
            
    
    def run(self, screen, event): 
        
        if event.type == pygame.KEYDOWN:

            if event.key in CONTROLS["M_DOWN"] and self.selected_index < (len(self.CONTROLS_DESC) - 1):
                self.selected_index = self._next_index()

            if event.key in CONTROLS["M_UP"] and self.selected_index > 0:
                self.selected_index = self._previous_index()

            if event.key in CONTROLS["M_SELECT"]:
               self.active_state = self.CONTROLS_DESC[self.selected_index][0]


    def display_frame(self, screen, background_image):
        font = pygame.font.SysFont('Arial', 30)
        BLACK = (0, 0, 0); WHITE = (255, 255, 255); RED = (255, 0, 0)
        selected_marker = ">"; unselected_marker = " "

        # clean game area
        screen.blit(background_image, (0, 0))

        
        for j in range(len(self.CONTROLS_DESC[0])):
            for i in range(len(self.CONTROLS_DESC)):
                if (j == 0 and i == self.selected_index): text = "{} {}".format(selected_marker, self.CONTROLS_DESC[i][j])
                else: text = "{} {}".format(unselected_marker, self.CONTROLS_DESC[i][j])

                draw_text(screen, text, font, BLACK, "L", 550 + j*200, 250 + i*50)

        pygame.display.update()


class Game(State):

    def __init__(self):
        State.__init__(self)
        self.active_state = "game"
        self.level = 0


        self.all_sprites = []
        self.all_sprites_group = pygame.sprite.Group()

        self.player = Player(speed = 8)
        self.player.rect.x = 100
        self.player.rect.bottom = 500
        self.all_sprites_group.add(self.player)

        ##self.keyword = Keyword()
        ##self.alphabet = Alphabet()
        self.score = Score(5)

        ##self.t_shuffle = 0

        self.game_over = False
        self.won_level = False
        self.new_level = True


    def process_events(self):
        if self.active_state == "Menu": return Menu()
        else: return self

    
    def run(self, screen, event):
        
        if self.new_level:
            self.level += 1
            self.score.update(self.level)
            ##self.keyword.assign_new(self.keyword.keywords_list)
            ##self.alphabet.reset()
            self.create_obstacles()
            self.player.rect.x = 100
            self.player.rect.bottom = 700
            self.new_level = False

        if not self.game_over:

            if not self.won_level:
                ##if pygame.time.get_ticks() > 15000 * self.t_shuffle:
                ##    self.t_shuffle += 1
                ##    self.create_obstacles()
                
                self.check_collisions()
                self.player.move(screen, event)
                self.player.fall()
                self.player.jump()
                self.check_game_result()

            # You won level screen - press any key to move to next level
            else: 
                self.won_level_continue(event)

        # Game over screen action - press any key and move to menu
        else:
            self.game_over_continue(event)
    
    # this is still working/testing version of this function...
    def create_obstacles(self):
        
        self.all_sprites_group = pygame.sprite.Group()
        self.all_sprites = []

        ground = Obstacle(image = pygame.Surface([2000, 50]), x = -50, y = 700)

        obstacle2 = Obstacle(image = pygame.Surface([400, 25]), x = 500, y = 675)

        obstacle3 = Obstacle(image = pygame.Surface([50, 700]), x = -25, y = 0)
        
        self.all_sprites.append(ground)
        self.all_sprites_group.add(ground)
        self.all_sprites.append(obstacle2)
        self.all_sprites_group.add(obstacle2)
        self.all_sprites.append(obstacle3)
        self.all_sprites_group.add(obstacle3)
               


    def check_collisions(self):
        var1 = (self.player.is_colliding_r, self.player.is_colliding_l, self.player.is_colliding_b, self.player.rect.bottom)
        # reset collision flags
        self.player.is_colliding_l = False
        self.player.is_colliding_r = False
        self.player.is_colliding_t = False
        self.player.is_colliding_b = False

        # set collision flags if player collides with an obstacle
        collision_list = pygame.sprite.spritecollide(self.player, self.all_sprites, False)
        
        for obstacle in collision_list:
            
            self.check_collision_r(obstacle)
            self.check_collision_l(obstacle)
            #self.check_collision_t(obstacle)
            self.check_collision_b(obstacle)


    # check collision player_right - obstacle_left
    def check_collision_r(self, obstacle):

        if pygame.sprite.collide_rect(self.player, obstacle) \
            and self.player.rect.left <= obstacle.rect.left \
            and self.player.rect.right >= obstacle.rect.left:

            self.player.stop_movement_x()
            self.player.is_colliding_r = True


    # check collision player_left - obstacle_right
    def check_collision_l(self, obstacle):

        if pygame.sprite.collide_rect(self.player, obstacle) \
            and self.player.rect.left <= obstacle.rect.right \
            and self.player.rect.right >= obstacle.rect.right:

            self.player.stop_movement_x()
            self.player.is_colliding_l = True


    # check collision player_bottom - obstacle_top - not working yet
    def check_collision_b(self, obstacle):

        # this condition is added to avoid changing y position when player collides with a corner of an obstacle (e.g., top left point)
        if not self.player.is_colliding_r and not self.player.is_colliding_l:

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
        if self.score.current_score == 0:
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

        pygame.display.update()

    
    def draw_main_game(self, screen, color):

        ## draw ground
        #self.draw_ground(screen, color)

        # draw alphabet letters
        self.all_sprites_group.draw(screen) 

        # Draw scores in right top corner
        self.draw_game_results(screen, self.score, color)

        # update player image in new position
        screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))


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
                             "Total score: {}".format(str(score.total_score)), 
                             "{} mistakes to hang!".format(str(score.current_score))]
        
        for n, result in enumerate(game_results_list):
            draw_text(screen, result, font, color, "R", screen.get_rect().width - 10, (10 + n*30))


def draw_text(screen, text, font, color, side, side_px, top_px):
    text_screen = font.render(text, False, color)
    text_screen_rect = text_screen.get_rect()
    text_screen_rect.top = top_px
    if side == "R": text_screen_rect.right = side_px
    if side == "L": text_screen_rect.left = side_px

    screen.blit(text_screen, text_screen_rect)