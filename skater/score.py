class Score:
    
    def __init__(self, max_trials):
        self.max_trials = max_trials
        self.current_score = max_trials
        self.total_score = 0


    def decrease_current(self, n = 1):
        self.current_score -= n


    def update(self, level):
        self.total_score += self.current_score
        self.current_score = self.max_trials

        # every three levels user receives one trial less with min number of trials smaller than max number of trials set in the game
        n = level // 4
        if n < self.max_trials:
            self.current_score -= n


    def reset(self):
        self.current_score = self.max_trials
        self.total_score = 0