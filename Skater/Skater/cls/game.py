import pygame
from pygame.locals import *
from cls.score import *

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, image_path):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):

    def __init__(self, image_path, speed = 0):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        #self.collider = pygame.transform.scale(self.image, (int(0.6 * self.rect.width), int(0.6 * self.rect.height)))
        #self.collider = self.collider.move((int(0.2 * self.rect.width), int(0.2 * self.rect.height)))
        #self.collider_rect = self.collider.get_rect()

        self.speed = speed
        self.v = 6
        self.m = 6
        self.is_jumping = False


    def move(self, screen, events):

        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_w):
                self.is_jumping = True

        #        if event.key == pygame.K_RIGHT and self.rect.x < (screen.get_size()[0] - self.rect.width): self.rect.x += self.speed
        #        if event.key == pygame.K_LEFT and self.rect.x > 400: self.rect.x += self.speed * (-1)
        #        if event.key == pygame.K_DOWN and self.rect.y < (screen.get_size()[1] - self.rect.height): self.rect.y += self.speed
        #        if event.key == pygame.K_UP and self.rect.y > 0: self.rect.y += self.speed * (-1)

        keystate = pygame.key.get_pressed()
        if keystate[K_RIGHT] and self.rect.x < (screen.get_size()[0] - self.rect.width): self.rect.x += self.speed
        if keystate[K_LEFT] and self.rect.x > 0: self.rect.x += self.speed * (-1)
        #if keystate[K_DOWN] and self.rect.y < (screen.get_size()[1] - self.rect.height): self.rect.y += self.speed
        #if keystate[K_UP] and self.rect.y > 0: self.rect.y += self.speed * (-1)

        #self.collider_rect.x += self.speed * direction[0]
        #self.collider_rect.y += self.speed * direction[1]


    def jump(self, ground_pos):
        if self.is_jumping:
            # Calculate force (F)
            F = self.m * self.v
            
            # Change position
            self.rect.y -= F
 
            # Change velocity
            self.v -= 1
 
            # If ground is reached, reset variables.
            if self.rect.y >= ground_pos:
                self.rect.y = ground_pos
                self.v = 8
                
                self.is_jumping = False


class State:
    
    def __init__(self):
        self.active_state = ""
        self.exit = False

    def process_events(self):
        raise NotImplementedError
    
    def run_level(self):
        raise NotImplementedError
    
    def display_frame(self, background_image):
        raise NotImplementedError

    def check_exit(self):
        if self.exit: return True
        else: return False


class Menu(State):
    
    OPTIONS = ["Play", "Exit"]

    def __init__(self):
        State.__init__(self)
        self.active_state = "menu"
        self.selected_index = 0


    def _next_index(self):
        max = len(self.OPTIONS)
        return (self.selected_index + 1) % max


    def _previous_index(self):
        max = len(self.OPTIONS)
        return (self.selected_index - 1) % max


    def process_events(self):

            if self.active_state == "game": return Game()
            elif self.active_state in ("menu", "next_level"): return self
            elif self.active_state == "exit": return self; self.exit = True

    
    def run_level(self, screen, events): 

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN and self.selected_index < (len(self.OPTIONS) - 1):
                    self.selected_index = self._next_index()

                if event.key == pygame.K_UP and self.selected_index > 0:
                    self.selected_index = self._previous_index()

                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                   if self.selected_index == 0: self.active_state = "game"
                   elif self.selected_index == 1: pygame.quit()


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


class Game(State):

    def __init__(self):
        State.__init__(self)
        self.active_state = "game"
        self.level = 0

        ##Keyword.initialize_list()

        self.all_sprites = []
        self.all_sprites_group = pygame.sprite.Group()

        self.player = Player("graphics/player.png", speed = 4)
        self.player.rect.x = 100
        self.player.rect.y = 550
        self.all_sprites_group.add(self.player)

        ##self.keyword = Keyword()
        ##self.alphabet = Alphabet()
        self.score = Score(5)

        ##self.t_shuffle = 0

        self.game_over = False
        self.won_level = False
        self.new_level = True

    def process_events(self):
        if self.active_state == "menu": return Menu()
        else: return self

    
    def run_level(self, screen, events):

        if self.new_level:
            self.level += 1
            self.score.update(self.level)
            ##self.keyword.assign_new(self.keyword.keywords_list)
            ##self.alphabet.reset()
            self.create_obstacles()
            self.player.rect.x = 100
            self.player.rect.y = 550
            self.new_level = False

        if not self.game_over:

            if not self.won_level:
                ##if pygame.time.get_ticks() > 15000 * self.t_shuffle:
                ##    self.t_shuffle += 1
                ##    self.create_obstacles()

                self.player.move(screen, events)
                self.player.jump(550)
                self.check_collision()
                self.check_game_result()

            # You won level screen - press any key to move to next level
            else: 
                self.won_level_continue(events)

        # Game over screen action - press any key and move to menu
        else:
            self.game_over_continue(events)
    
    # all_letters list will contain available alphabet letters and will be used in player-letter collision detection 
    def create_obstacles(self):
        
        self.all_sprites_group = pygame.sprite.Group()
        self.all_sprites = []

        obstacle = Obstacle("graphics/obstacle.png")
        obstacle.rect.x = 700
        obstacle.rect.y = 300

        self.all_sprites.append(obstacle)
        self.all_sprites_group.add(obstacle)


    def check_collision(self):
        #Check if there is a colision player - letter and if yes then update hidden keyword on screen, update alphabet and scores
        collision_list = pygame.sprite.spritecollide(self.player, self.all_sprites, False)

        for obstacle in collision_list:
            self.all_sprites_group.remove(obstacle)
            self.all_sprites.remove(obstacle)
            self.score.decrease_current()


    def check_game_result(self):
        if self.score.current_score == 0:
            self.game_over = True

    
    def game_over_continue(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.active_state = "menu"
                elif event.key == pygame.K_n:
                    self.exit = True


    def won_level_continue(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y: 
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


    def draw_game_results(self, screen, score, color):
        font = pygame.font.SysFont('Arial', 20)
        game_results_list = ["Level: {}".format(self.level), 
                             "Total score: {}".format(str(score.total_score)), 
                             "{} mistakes to hang!".format(str(score.current_score))]
        
        for n, result in enumerate(game_results_list):
            draw_text(screen, result, font, color, "R", 1550, (10 + n*30))


def draw_text(screen, text, font, color, side, side_px, top_px):
    text_screen = font.render(text, False, color)
    text_screen_rect = text_screen.get_rect()
    text_screen_rect.top = top_px
    if side == "R": text_screen_rect.right = side_px
    if side == "L": text_screen_rect.left = side_px

    screen.blit(text_screen, text_screen_rect)