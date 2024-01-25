from constants import Tile, Actions, BoardMoves, GameState, GameText
import numpy as np
import random
from pynput import keyboard
from typing import Union
import textwrap

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


class Score:
    def __init__(self, score: int = 0):
        self.score: int  = score
    
    def __str__(self):
        return f"{self.score}"
    
    def addPointsToScore(self, increment):
        self.score += increment

class GameLogic:
    def __init__(self,board: Board = Board(),score: Score = Score()):
        #Initialize Game Variables
        self.board: Board = board
        self.score: Score = score
        self.state: GameState = GameState.START_SCREEN

        #Initialize Keyboard Variables then run thread separate from the GameLogic Instance
        self.already_holding_a_key: bool = False
        self.already_held_key: Union[None,keyboard.Key]
        self.escape_pressed_once: bool = False
        self.valid_actions = [action.value for action in Actions]
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def startKeyboardListener(self):
        with self.listener as listener:
            listener.join()

    def stopKeyboardListener(self):
        self.listener.stop()

    def on_press(self,key):
        if key in self.valid_actions and not self.already_holding_a_key:
            self.already_holding_a_key = True
            self.already_held_key = key
    
    def on_release(self,key):
        if key in self.valid_actions and key == self.already_held_key:
            self.already_held_key = None
            self.already_holding_a_key = False       
            self.performAction(key)

    def performAction(self,action: Actions):
        if self.state == GameState.START_SCREEN and action in self.valid_actions and action != keyboard.Key.esc:
            print("game started!")
            self.state = GameState.PLAYING
            self.board.generateNewTile()
            self.printBoard()  
        elif action == Actions.UP.value:
            self.escape_pressed_once = False
            points_earned = self.doBoardMove(BoardMoves.UP)
            self.score.addPointsToScore(points_earned)
            # self.board.generateNewTile()
            self.printBoard()
            print(f"earned {points_earned} points. score:{self.score}")
        elif action == Actions.DOWN.value:
            self.escape_pressed_once = False
            points_earned = self.doBoardMove(BoardMoves.DOWN)
            self.score.addPointsToScore(points_earned)
            # self.board.generateNewTile()
            self.printBoard()
            print(f"earned {points_earned} points. score:{self.score}")
        elif action == Actions.LEFT.value:
            self.escape_pressed_once = False
            points_earned = self.doBoardMove(BoardMoves.LEFT)
            self.score.addPointsToScore(points_earned)
            # self.board.generateNewTile()
            self.printBoard()
            print(f"earned {points_earned} points. score:{self.score}")
        elif action == Actions.RIGHT.value:
            self.escape_pressed_once = False
            points_earned = self.doBoardMove(BoardMoves.RIGHT)
            self.score.addPointsToScore(points_earned)
            # self.board.generateNewTile()
            self.printBoard()
            print(f"earned {points_earned} points. score:{self.score}")
        elif action == Actions.ESCAPE.value:
            if not self.escape_pressed_once:
                self.escape_pressed_once = True
                print("Are you sure you want to quit?")
            else:
                self.quitGame()

    def doBoardMove(self,boardMove: BoardMoves) -> int:
        points_earned: int = 0
        if boardMove.value == "UP":
            return self.board.upMove()
        elif boardMove.value == "DOWN":
            return self.board.downMove()
        elif boardMove.value == "LEFT":
            return self.board.leftMove()
        elif boardMove.value == "RIGHT":
            return self.board.rightMove()
        else:
            raise RuntimeError("This should never happen.")    


    def startGame(self):
        print(textwrap.dedent(GameText.INTRO.value))

    def quitGame(self) -> None:
        self.state = GameState.ENDED
        print(textwrap.dedent(GameText.QUIT.value))
        self.stopKeyboardListener()

    def printBoard(self):
        print(self.board)
    
    def printScore(self):
        print(self.score)

def main():
    try:    
        game = GameLogic()
        game.startGame()
        game.startKeyboardListener()
    except KeyboardInterrupt:
        pass
        # print("Keyboard interrupt ignored. Please press <ESC> key twice in a row :)")


if __name__ == "__main__":
    main()