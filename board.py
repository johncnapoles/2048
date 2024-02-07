import random
from constants import Tile
import numpy as np

class Board:
    def __init__(self,rows=4,columns=4):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows,columns),dtype=int)
        self.moveCount = 0
        # self.occupiedTiles = set() 
        self.maxOccupiedTileCount = rows*columns

    def __str__(self) -> str:
        return f"{self.board}"

    def isAllTilesOccupied(self) -> bool:        
        for row in self.board:
            for element in row:
                if element == 0:
                    return False
        return True

    def generateNewTile(self) -> 'tuple[int,int]':
        #Keep Repeating
        while(True):
            row_index = random.randint(0,self.rows-1)
            column_index = random.randint(0,self.columns-1)
            #Until Unique Tile is Generated
            if self.board[row_index][column_index] == 0:
                #Place tile in board        
                self.board[row_index][column_index] = Tile.TWO.value
                #Return new tile coordinate
                return (row_index,column_index) 

    def triggerLoss(self) -> None:
        """
        is this loss?
        """
        print(GameText.LOSE.value)

    def leftMove(self) -> int:
        points_earned: int = 0
        #for every row
        for i in range(self.rows):
            flag_row_finished = False
            while not flag_row_finished:
                flag_swap_made = False
                #start from left look one to the right
                for j in range(0,self.columns-1,1):
                    # if tile to right is 0, do nothing
                    if self.board[i][j+1] == 0:
                        continue
                    # if tile to right is something and current tile is 0, move
                    elif self.board[i][j] == 0:
                        self.board[i][j] = self.board[i][j+1]
                        self.board[i][j+1] = 0

                        flag_swap_made = True
                    # if current tile == tile to right, set tile to right as 0, current is sum
                    elif self.board[i][j] == self.board[i][j+1]:
                        self.board[i][j] = self.board[i][j+1]*2
                        self.board[i][j+1] = 0
                        points_earned = self.board[i][j]
                        flag_swap_made = True
                    # if current tile != tile to right, do nothing
                    elif self.board[i][j+1] != self.board[i][j]:
                        continue
                #If no swaps was made. No More need to repeat to check
                if not flag_swap_made:
                    flag_row_finished = True
        return points_earned

    def rightMove(self) -> int:
        points_earned: int = 0
        #for every row
        for i in range(self.rows):
            flag_row_finished = False
            while not flag_row_finished:
                flag_swap_made = False
                #start from right look one to the left
                for j in range(self.columns-1,0,-1):
                    # if tile to left is 0, do nothing
                    if self.board[i][j-1] == 0:
                        continue
                    # if tile to left is something and current tile is 0, move
                    elif self.board[i][j] == 0:
                        self.board[i][j] = self.board[i][j-1]
                        self.board[i][j-1] = 0
                        flag_swap_made = True
                    # if current tile == tile to right, set tile to right as 0, current is sum
                    elif self.board[i][j] == self.board[i][j-1]:
                        self.board[i][j] = self.board[i][j-1]*2
                        self.board[i][j-1] = 0
                        points_earned = self.board[i][j]
                        flag_swap_made = True
                    # if current tile != tile to right, do nothing
                    elif self.board[i][j-1] != self.board[i][j]:
                        continue
                #If no swaps was made. No More need to repeat to check
                if not flag_swap_made:
                    flag_row_finished = True
        return points_earned

    def downMove(self) -> int:
        points_earned: int = 0
        #for every column
        for column in range(self.columns):
            flag_row_finished = False
            while not flag_row_finished:
                flag_swap_made = False
                #start from bottom row to top row
                for row in range(self.rows-1,0,-1):
                    # if tile above is 0, do nothing
                    if self.board[row-1][column] == 0:
                        continue
                    # if tile above is something and current tile is 0, move
                    elif self.board[row][column] == 0:
                        self.board[row][column] = self.board[row-1][column]
                        self.board[row-1][column] = 0

                        flag_swap_made = True
                    # if current tile == tile above, set tile to right as 0, current is sum
                    elif self.board[row][column] == self.board[row-1][column]:
                        self.board[row][column] = self.board[row-1][column]*2
                        self.board[row-1][column] = 0

                        points_earned = self.board[row][column]
                        flag_swap_made = True
                    # if current tile != tile to right, do nothing
                    elif self.board[row-1][column] != self.board[row][column]:
                        continue
                #If no swaps was made. No More need to repeat to check
                if not flag_swap_made:
                    flag_row_finished = True
        return points_earned

    def upMove(self) -> int:
        points_earned: int = 0
        #for every column
        for column in range(self.columns):
            flag_row_finished = False
            while not flag_row_finished:
                flag_swap_made = False
                #start from top row to bottom row
                for row in range(0,self.rows-1,1):
                    # if tile below is 0, do nothing
                    if self.board[row+1][column] == 0:
                        continue
                    # if tile below is something and current tile is 0, move
                    elif self.board[row][column] == 0:
                        self.board[row][column] = self.board[row+1][column]
                        self.board[row+1][column] = 0

                        flag_swap_made = True
                    # if current tile == tile above, set tile to right as 0, current is sum
                    elif self.board[row][column] == self.board[row+1][column]:
                        self.board[row][column] = self.board[row+1][column]*2
                        self.board[row+1][column] = 0

                        points_earned = self.board[row][column]
                        flag_swap_made = True
                    # if current tile != tile to right, do nothing
                    elif self.board[row+1][column] != self.board[row][column]:
                        continue
                #If no swaps was made. No More need to repeat to check
                if not flag_swap_made:
                    flag_row_finished = True
        return points_earned
