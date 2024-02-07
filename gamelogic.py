from constants import Tile, Actions, BoardMoves, GameState, GameText
from score import Score
from board import Board
import textwrap
from typing import Union
from pynput import keyboard

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
