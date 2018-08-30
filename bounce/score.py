class Score:
    
    """
    Points are added when colliding with collectables
    Meters equal to the number of pixels player went up
    """

    def __init__(self, init_number_of_lives = 1):
        self.init_number_of_lives = init_number_of_lives
        self.number_of_lives = init_number_of_lives
        self.points = 0
        self.meters = 0


    def decrease_lives(self):
        self.number_of_lives -= 1

    def add_points(self, points = 10):
        self.points += points

    def update_meters(self, meters):
        self.meters = int(meters / 10)


    def reset(self):
        self.number_of_lives = self.init_number_of_lives
        self.points = 0
        self.meters = 0
