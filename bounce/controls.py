from silnik.image import Image
from silnik.rendering.text import Text
from silnik.rendering.colors import Colors

from .destination import Destination
from .state import *


class Controls(State):
    
    # dictionary with assignment and descriptions of control keys
    CONTROLS_DESC = [
        ["Right", "D / Right Arrow"],
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
        selected_marker = ">"
        unselected_marker = " "

        screen.fill(Colors.WHITE, (0, 0, screen.get_size()[0], screen.get_size()[1]))

        for i, pair in enumerate(self.CONTROLS_DESC):
            description, key = pair
            marker = selected_marker if i == self.selected_index else unselected_marker
            content = "{} {}    {}".format(marker, description, key)
            text = Text(content, font_color=Colors.BLACK, font_size=25)
            renderable_text = Image.from_pyimage(text.pre_render())
            renderable_text.shape.x = 50
            renderable_text.shape.y = 250 + i * 100
            renderable_text.render(screen)

        pygame.display.update()
