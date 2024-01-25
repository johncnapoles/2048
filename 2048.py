from constants import Tile, Actions, GameState, GameText
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
        self.occupiedTiles = set()
        self.maxOccupiedTileCount = rows*columns

    def __str__(self) -> str:
        return f"{self.board}"

    def isAllTilesOccupied(self) -> bool:
        #TODO 1. Logic should check if there is no possible future moves in gamelogic.
        if(len(self.occupiedTiles) == self.maxOccupiedTileCount):
            print("GG no re")
            return False
        return True

    def generateNewTile(self) -> 'tuple[int,int]':
        """
            1. Generate Tile in unoccupied space
            2. Place Tile in self.board
            3. Return new tile coordinates
        """
        emptyTileGenerated: bool = False
        coordinate: tuple[int,int] = (0,0)
        
        if not self.isAllTilesOccupied(): # dEfEnSiVe ProGraMiNg
            self.triggerLoss()

        while(not emptyTileGenerated):
            coordinate = (random.randint(0,3),random.randint(0,3))
            if coordinate not in self.occupiedTiles:
                self.occupiedTiles.add(coordinate)
                emptyTileGenerated = True
                break

        self.board[coordinate[0],coordinate[1]] = Tile.TWO.value

        return coordinate

    def triggerLoss(self) -> None:
        """
        is this loss?
        """
        print(GameText.LOSE.value)

class Score:
    def __init__(self, score=0):
        self.score = score
    
    def __str__(self):
        return f"{self.score}"
    
    def updateScore(self, increment):
        self.score += increment

class GameLogic:
    def __init__(self,board: Board = Board(),score: Score = Score()):
        #Initialize Game Variables
        self.board: Board = board
        self.score: int = score
        self.state: GameState = GameState.START_SCREEN
        
        #Initialize Keyboard Variables
        self.already_holding_a_key: bool = False
        self.already_held_key: Union[None,keyboard.Key]
        self.escape_pressed_once: bool = False
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.valid_actions = [action.value for action in Actions]

        self.startGame()

    def startKeyboardListener(self):
        with self.listener:
            self.listener.join()

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
            print(f'U pressed and released.')
        elif action == Actions.DOWN.value:
            self.escape_pressed_once = False
            print(f'D pressed and released.')
        elif action == Actions.LEFT.value:
            self.escape_pressed_once = False
            print(f'L pressed and released.')
        elif action == Actions.RIGHT.value:
            self.escape_pressed_once = False
            print(f'R pressed and released.')
        elif action == keyboard.Key.esc:
            if not self.escape_pressed_once:
                self.escape_pressed_once = True
                print("Are you sure you want to quit?")
            else:
                self.quitGame()

    def startGame(self):
        print(textwrap.dedent(GameText.INTRO.value))
        self.startKeyboardListener()

    def quitGame(self) -> None:
        self.state = GameState.ENDED
        print(textwrap.dedent(GameText.QUIT.value))
        self.listener.stop()

    def printBoard(self):
        print(self.board)

def main():
    game = GameLogic()

if __name__ == "__main__":
    main()