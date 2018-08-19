from enum import Enum

class Destination(Enum):
    """
    A list of predefined routing destinations.
    """
    MENU = 1
    CONTROLS = 2
    GAME = 3
    EXIT = 4