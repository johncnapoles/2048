class Score:
    def __init__(self, score: int = 0):
        self.score: int  = score
    
    def __str__(self):
        return f"{self.score:>{6}}"
    
    def addPointsToScore(self, increment):
        self.score += increment