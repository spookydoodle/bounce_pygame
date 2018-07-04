import pygame
from pygame.locals import *
from cls.score import *

# M = Menu controls, G = Game controls
CONTROLS = {"M_UP" : [pygame.K_w, pygame.K_UP],
            "M_DOWN" : [pygame.K_s, pygame.K_DOWN],
            "M_SELECT" : [pygame.K_KP_ENTER, pygame.K_RETURN],

            "G_RIGHT" : [pygame.K_d, pygame.K_RIGHT],
            "G_LEFT" : [pygame.K_a, pygame.K_LEFT],
            "G_MANUAL" : [pygame.K_w, pygame.K_UP],
            "G_OLLIE" : [pygame.K_SPACE],
            "G_KICKFLIP" : [],
            "G_BACKFLIP" : [],
            "G_GRIND" : [],

            "QUIT" : [pygame.K_q],
            "YES" : [pygame.K_y],
            "NO" : [pygame.K_n]
            }


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, image_path = None, image = None):
        super().__init__()

        if image_path != None:
            self.image = pygame.image.load(image_path).convert_alpha()
        else: 
            self.image = image
            self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):

    # these parameters are used to decrease velocity when decelerating
    DRAG = 0.7
    ZERO = 0.000001

    # gravity parameter used for relating jumping velocity to main velocity G * v
    G = 0.8
    
    # elasticity parameter used to decrease velocity when hitting the ground
    ELASTICITY = 0.8


    # dictionary with paths to player images for each action/trick
    IMAGES = {"MAIN" : "graphics/player.png", 
              "MANUAL" : "graphics/player_manual.png"
              }

    def __init__(self, speed = 0):
        super().__init__()

        self.image = pygame.image.load(self.IMAGES["MAIN"]).convert_alpha()
        self.rect = self.image.get_rect()

        #self.collider = pygame.transform.scale(self.image, (int(0.6 * self.rect.width), int(0.6 * self.rect.height)))
        #self.collider = self.collider.move((int(0.2 * self.rect.width), int(0.2 * self.rect.height)))
        #self.collider_rect = self.collider.get_rect()

        # speed is used for movement to left/right
        self.speed = speed

        # acceleration, velocity, mass - used for acceleration and deceleration. 
        # separate velocities for movement on x axis (right/left) and y axis (jump)
        self.a = 2
        self.v = self.v0 = 8
        self.v_jump = self.G * self.v0
        self.m = 5
        self.is_jumping = False
        self.is_falling = False
        self.is_decelerating = False

        # flags used to perform tricks
        self.is_manual = False

        # these parameters are used to stop the player after hitting  obstacle on horizontal axis (x)
        self.is_colliding_r = False
        self.is_colliding_l = False
        self.is_colliding_t = False
        self.is_colliding_b = False

        # these parameters are used to determine direction for accelerating/decelerating when user stops skating; 
        # 1 = right/up, -1 = left/down, 0 = no movement
        self.moving_direction_x = 0
        self.moving_direction_y = 1


    # function to load sprite images for each action/trick
    def load_image(self, path):
        self.image = pygame.image.load(path).convert_alpha()

    # handle user input
    def move(self, screen, events):

        # set moving_direction_x parameter based on user input, except for when skater is in the air (is_jumping parameter)
        keystate = pygame.key.get_pressed()

        if not self.is_jumping:

            # here need to change to also use the dictionary CONTROLS - tbd later
            if (keystate[K_RIGHT] or keystate[K_d]) and self.rect.x < (screen.get_size()[0] - self.rect.width):
                self.moving_direction_x = 1

            if (keystate[K_LEFT] or keystate[K_a]) and self.rect.x > 0: 
                self.moving_direction_x = -1


        # set flags for tricks based on user input
        if keystate[K_UP]: self.is_manual = True
        else: self.is_manual = False


        # set flags for jumping based on user input and for deceleration if user stops pressing movement buttons
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in CONTROLS["G_OLLIE"]:
                    self.is_jumping = True

            elif event.type == pygame.KEYUP:
                self.is_decelerating = True
                self.is_manual = False


        # call movement functions after handling user input
        self.call_movement_functions()

    
    def call_movement_functions(self):
        self.accelerate()
        self.decelerate()
        self.handle_images()


    def accelerate(self):
        if (not self.is_colliding_r and self.moving_direction_x > 0) \
        or (not self.is_colliding_l and self.moving_direction_x < 0):
            self.rect.x += self.speed * self.moving_direction_x
            #self.rect.x += self.v * self.v / self.a * self.moving_direction_x

            #if self.v < 10:
            #    self.v *= 1.2
        

    def decelerate(self):

        if not self.is_colliding_r:

            if self.v > self.ZERO and self.is_decelerating:
                self.rect.x += self.v * self.v / self.a * self.moving_direction_x
            
                # decrease velocity using drag parameter but only if on the ground
                if not self.is_jumping:
                    self.v *= self.DRAG 

            # if velocity reaches 0.00001 reset to initial velocity value v0
            elif self.v <= self.ZERO:
                self.stop_movement_x()



    def jump(self, ground_pos_y):
        if self.is_jumping:
            # Calculate force (F)
            F = self.m * self.v_jump
            
            # Change position
            self.rect.y -= F
 
            # Change velocity
            self.v_jump -= 1


            ## this code was supposed to make jumps smoother

            #if not self.is_falling:
            #    self.v_jump *= self.DRAG
            #else:
            #    self.v_jump = (-1) * abs(self.v_jump) * 1/self.DRAG

            #if self.v_jump < self.ZERO:
            #    self.is_falling = True


            # If ground is reached, reset variables.
            if self.rect.y >= ground_pos_y:
                self.stop_movement_y()


    def stop_movement_x(self):
        self.is_decelerating = False
        self.moving_direction_x = 0
        self.v = self.v0

    
    def stop_movement_y(self):
        #self.rect.y = ground_pos_y
        self.v_jump = self.G * self.v0
        self.v *= self.ELASTICITY
        self.is_jumping = False
        self.is_falling = False


    def handle_images(self):
        if self.is_manual: self.image = pygame.image.load(self.IMAGES["MANUAL"]).convert_alpha()
        else: self.image = pygame.image.load(self.IMAGES["MAIN"]).convert_alpha()


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

    
    def run(self, screen, events): 
        
        for event in events:
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
            
    
    def run(self, screen, events): 
        
        for event in events:
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

        ##Keyword.initialize_list()

        self.all_sprites = []
        self.all_sprites_group = pygame.sprite.Group()

        self.player = Player(speed = 8)
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
        if self.active_state == "Menu": return Menu()
        else: return self

    
    def run(self, screen, events):
        
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
                
                self.check_collisions()
                self.player.move(screen, events)
                self.player.jump(550)
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

        obstacle = Obstacle(image_path = "graphics/obstacle.png")
        obstacle.rect.x = -40
        obstacle.rect.y = 650

        obstacle2 = Obstacle(image = pygame.Surface([600, 50]))
        obstacle2.rect.x = 400
        obstacle2.rect.y = 650

        self.all_sprites.append(obstacle)
        self.all_sprites_group.add(obstacle)
        
        self.all_sprites.append(obstacle2)
        self.all_sprites_group.add(obstacle2)


    def check_collisions(self):
        collision_list = pygame.sprite.spritecollide(self.player, self.all_sprites, False)
    
        for obstacle in collision_list:
            
            self.check_collision_r(obstacle)
            self.check_collision_l(obstacle)

    # check collision player_right - obstacle_left
    def check_collision_r(self, obstacle):
        if (self.player.rect.collidepoint(obstacle.rect.midleft) \
            or self.player.rect.collidepoint(obstacle.rect.topleft) \
            or self.player.rect.collidepoint(obstacle.rect.bottomleft)) \
            and (self.player.rect.x + self.player.rect.width) >= obstacle.rect.x:
            self.player.stop_movement_x()
            self.player.is_colliding_r = True
        
        else:
            self.player.is_colliding_r = False


    # check collision player_left - obstacle_right
    def check_collision_l(self, obstacle):
        if (self.player.rect.collidepoint(obstacle.rect.midright) \
            or self.player.rect.collidepoint(obstacle.rect.topright) \
            or self.player.rect.collidepoint(obstacle.rect.bottomright)) \
            and self.player.rect.x <= (obstacle.rect.x + obstacle.rect.width):

            self.player.stop_movement_x()
            self.player.is_colliding_l = True

        else:
            self.player.is_colliding_l = False

    ## check collision player_bottom - obstacle_top - not working yet
    #def check_collision_b(self, obstacle):
    #    if self.player.rect.colliderect(obstacle.rect) \
    #        and self.player.rect.x <= (obstacle.rect.x + obstacle.rect.height) \
    #        and self.player.rect.x <= (obstacle.rect.x + obstacle.rect.width):

    #        self.player.stop_movement_y()
    #        self.player.is_colliding_b = True  


    def check_game_result(self):
        if self.score.current_score == 0:
            self.game_over = True

    
    def game_over_continue(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in CONTROLS["YES"]:
                    self.active_state = "Menu"
                elif event.key == pygame.K_n:
                    self.exit = True


    def won_level_continue(self, events):
        for event in events:
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

        # draw ground
        self.draw_ground(screen, color)

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