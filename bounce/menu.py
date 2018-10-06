from silnik.image import Image
from silnik.rendering.text import Text

from .constants import Colors
from .state import *
from .destination import Destination


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


    def next_destination(self):

            if self.active_state == "Play": return Destination.GAME
            elif self.active_state == "Controls" : return Destination.CONTROLS
            elif self.active_state == "Exit": return Destination.EXIT

    
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

        ## clean game area
        #screen.blit(background_image.raw_image, (0, 0))
        screen.fill(WHITE)

        for i in range(len(self.OPTIONS)):
            if i == self.selected_index:
                content = "{} {}".format(selected_marker, self.OPTIONS[i])
            else:
                content = "{} {}".format(unselected_marker, self.OPTIONS[i])

            text = Text(content, font_color=BLACK, font_size=40)
            renderable_text = Image.from_pyimage(text.pre_render())
            renderable_text.shape.x = 50
            renderable_text.shape.y = 250 + i * 100
            renderable_text.render(screen)

        pygame.display.update()