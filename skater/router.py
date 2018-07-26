from .destination import Destination
from .state import State

class Router:
    def __init__(self, destinations):
        """
        Destinations has to be a dictionary of { Destination: [State subclass] }

        Adds a layer of indirection between States transitioning between each other.
        """
        assert all(
            isinstance(key, Destination) and issubclass(value, State)
            for key, value in destinations.items()), "Invalid destinations: {}".format(destinations)
        
        self.destinations = destinations

    def route(self, destination):
        """
        Finds a matching destination, returns a new instance of it.
        """
        assert destination in list(Destination), "{} value expected, got {}".format(Destination, destination)
        return self.destinations[destination]()