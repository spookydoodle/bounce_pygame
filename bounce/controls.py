from .destination import Destination
from .state import *


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


    def next_destination(self):

            if self.active_state == "Back": return Destination.MENU
            
    
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
        #screen.blit(background_image.raw_image, (0, 0))
        screen.fill(WHITE, (0, 0, screen.get_size()[0], screen.get_size()[1]))

        
        for j in range(len(self.CONTROLS_DESC[0])):
            for i in range(len(self.CONTROLS_DESC)):
                if (j == 0 and i == self.selected_index): text = "{} {}".format(selected_marker, self.CONTROLS_DESC[i][j])
                else: text = "{} {}".format(unselected_marker, self.CONTROLS_DESC[i][j])

                draw_text(screen, text, font, BLACK, "L", 550 + j*200, 250 + i*50)

        pygame.display.update()
