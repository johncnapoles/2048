import random
from constants import Tile
import numpy as np
from typing import Dict
class Board:
    def __init__(self,rows=4,columns=4):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows,columns),dtype=int)
        self.maxOccupiedTileCount = rows*columns

    def __str__(self) -> str:
        return f"{self.board}"

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

    def checkPossibleMoves(self) -> Dict[str,bool]:
        """
        Check every tile in the board. 
        FOR EACH move, check IF ANY tile can [move] or [merge] without index exceptions
        Return an array of all the possible moves
        """
        left_possible = False
        right_possible = False
        up_possible = False
        down_possible = False

        for row_index in range(self.rows):
            for column_index in range(self.columns):
                if self.board[row_index][column_index] == 0:
                    continue
                if not left_possible:
                    if self.checkLeftForTile(row_index,column_index):
                        left_possible = True
                if not right_possible:
                    if self.checkRightForTile(row_index,column_index):
                        right_possible = True
                if not up_possible:
                    if self.checkUpForTile(row_index,column_index):
                        up_possible = True
                if not down_possible:
                    if self.checkDownForTile(row_index,column_index):
                        down_possible = True
                if left_possible and right_possible and up_possible and down_possible:
                    #Stop early. all is found
                    break
        
        return {
            'left': left_possible,
            'right': right_possible,
            'up': up_possible,
            'down': down_possible
        }

    def checkLeftForTile(self,row_index,column_index) -> bool:
        #edge case, literally
        if column_index == 0:
            return False
        #normal case
        tile_value = self.board[row_index][column_index]
        other_tile_value = self.board[row_index][column_index-1]
        if other_tile_value == 0 or other_tile_value == tile_value:
            # print(f"left possible for {row_index}{column_index}")
            return True
        else:
            # print(f"left NOT possible for {row_index}{column_index}")
            return False

    def checkRightForTile(self,row_index,column_index) -> bool:
        #edge case
        if column_index == self.columns-1:
            return False
        #normal case
        tile_value = self.board[row_index][column_index]
        other_tile_value = self.board[row_index][column_index+1]
        if other_tile_value == 0 or other_tile_value == tile_value:
            return True
        else:
            return False

    def checkUpForTile(self,row_index,column_index) -> bool:
        #edge case
        if row_index == 0:
            return False
        #normal case
        tile_value = self.board[row_index][column_index]
        other_tile_value = self.board[row_index-1][column_index]
        if other_tile_value == 0 or other_tile_value == tile_value:
            return True
        else:
            return False

    def checkDownForTile(self,row_index,column_index) -> bool:
        #edge case
        if row_index == self.rows-1:
            return False
        #normal case
        tile_value = self.board[row_index][column_index]
        other_tile_value = self.board[row_index+1][column_index]
        if other_tile_value == 0 or other_tile_value == tile_value:
            return True
        else:
            return False

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
