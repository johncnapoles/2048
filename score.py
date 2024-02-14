class Score:
    def __init__(self, score: int = 0) -> None:
        self.score: int  = score
    
    def __str__(self) -> str:
        return f"{self.score:>{6}}"
    
    def addPointsToScore(self, increment) -> None:
        self.score += increment

    def resetScore(self) -> None:
        self.score = 0