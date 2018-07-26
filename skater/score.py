class Score:
    
    # player receives initial number of lives, number_of_lives represents current number of lives
    # total_score is increased once player does skating tricks 
    def __init__(self, init_number_of_lives):
        self.init_number_of_lives = init_number_of_lives
        self.number_of_lives = init_number_of_lives
        self.total_score = 0


    def decrease_lives(self):
        self.number_of_lives -= 1

    
    # the greater the level, more points player receives for tricks
    def add_points(self, level):
        self.total_score += 10 * level


    def reset(self):
        self.number_of_lives = self.init_number_of_lives
        self.total_score = 0