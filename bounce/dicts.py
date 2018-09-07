import pygame


# M = Menu controls, G = Game controls
CONTROLS = {"M_UP" : [pygame.K_w, pygame.K_UP],
            "M_DOWN" : [pygame.K_s, pygame.K_DOWN],
            "M_SELECT" : [pygame.K_KP_ENTER, pygame.K_RETURN],

            "G_RIGHT" : [pygame.K_d, pygame.K_RIGHT],
            "G_LEFT" : [pygame.K_a, pygame.K_LEFT],
            "G_MANUAL" : [pygame.K_w, pygame.K_UP],
            "G_OLLIE" : [pygame.K_SPACE],
            "G_SHOOT" : [pygame.K_SPACE],
            "G_BACKFLIP" : [],
            "G_GRIND" : [],

            "QUIT" : [pygame.K_q],
            "YES" : [pygame.K_y],
            "NO" : [pygame.K_n]
            }