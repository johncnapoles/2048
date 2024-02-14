from constants import Actions, BoardMoves, GameState, GameText
from score import Score
from board import Board
import textwrap
from typing import Union
from pynput import keyboard

class GameLogic:
    def __init__(self,board: Board = Board(),score: Score = Score()) -> None:
        #Initialize Game Variables
        self.board: Board = board
        self.score: Score = score
        self.state: GameState = GameState.START_SCREEN

        self.turnCount = 0
        self.possible_moves = []

        #Initialize Keyboard Variables then run thread separate from the GameLogic Instance
        self.already_holding_a_key: bool = False
        self.already_held_key: Union[None,keyboard.Key]
        self.escape_pressed_once: bool = False
        self.valid_actions = [action.value for action in Actions]
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def startKeyboardListener(self) -> None:
        with self.listener as listener:
            listener.join()

    def stopKeyboardListener(self) -> None:
        self.listener.stop()

    def on_press(self,key) -> None:
        if key in self.valid_actions and not self.already_holding_a_key:
            self.already_holding_a_key = True
            self.already_held_key = key
    
    def on_release(self,key) -> None:
        if key in self.valid_actions and key == self.already_held_key:
            self.already_held_key = None
            self.already_holding_a_key = False
            self.performAction(key)

    def triggerUpdateTurn(self, points_earned) -> None:
        """
        triggered after every move
        1. Generate New Tile
        2. Print Board
        3. Print Points Gained. Update and Print Score Count
        4. Update and Print Turn Count
        5. Update possible moves - will be used to see if next move is legal
        6. Trigger Lose condition if no possible moves
        """
        #1
        self.board.generateNewTile()

        #2
        print(self.board)

        #3
        self.score.addPointsToScore(points_earned)
        print(f"earned {points_earned:>{3}} points. score:{self.score}")

        #4
        self.turnCount += 1
        print(f"turn {self.turnCount:>{3}}")

        #5
        self.possible_moves = [move for move,legal in self.board.checkPossibleMoves().items() if legal]
        
        #6
        if len(self.possible_moves) == 0:
            self.triggerLoss()

    def performAction(self,action: Actions) -> None:
        #First legal action input starts the game
        if self.state == GameState.START_SCREEN and action in self.valid_actions and action != keyboard.Key.esc:
            self.state = GameState.PLAYING
            self.board.generateNewTile()
            self.printBoard()
            self.possible_moves = [move for move,legal in self.board.checkPossibleMoves().items() if legal]
        #Subsequent legal action translates to a move that generates points, and a new tile
        elif action == Actions.UP.value and self.state == GameState.PLAYING and 'up' in self.possible_moves:
            self.escape_pressed_once = False
            points_earned = self.doBoardMove(BoardMoves.UP)
            self.triggerUpdateTurn(points_earned)
        elif action == Actions.DOWN.value and self.state == GameState.PLAYING and 'down' in self.possible_moves:
            self.escape_pressed_once = False
            points_earned = self.doBoardMove(BoardMoves.DOWN)
            self.triggerUpdateTurn(points_earned)
        elif action == Actions.LEFT.value and self.state == GameState.PLAYING and 'left' in self.possible_moves:
            self.escape_pressed_once = False
            points_earned = self.doBoardMove(BoardMoves.LEFT)
            self.triggerUpdateTurn(points_earned)
        elif action == Actions.RIGHT.value and self.state == GameState.PLAYING and 'right' in self.possible_moves:
            self.escape_pressed_once = False
            points_earned = self.doBoardMove(BoardMoves.RIGHT)
            self.triggerUpdateTurn(points_earned)
        
        elif action == Actions.R.value and self.state == GameState.PLAYING:
            self.state = GameState.RETRYING
            self.printRetryMessage()
        
        # Handle RETRYING State
        elif self.state == GameState.RETRYING:
            if action == Actions.Y.value:
                self.restartGame()
            elif action == Actions.N.value:
                print(textwrap.dedent(GameText.RESUME.value))
                self.printBoard()
                self.state = GameState.PLAYING
            else:
                print(textwrap.dedent(GameText.INVALIDRETRYINPUT.value))
                self.printRetryMessage()
        # Handle ENDED State
        elif self.state == GameState.ENDED:
            if action == Actions.Y.value:
                self.restartGame()
            elif action == Actions.N.value:
                self.quitGame()
            else:
                print(textwrap.dedent(GameText.INVALIDRETRYINPUT.value))
                self.printRetryMessage()
        # Handle Quit Logic
        elif action == Actions.ESCAPE.value:
            if not self.escape_pressed_once:
                self.escape_pressed_once = True
                print("Are you sure you want to quit?")
            else:
                self.quitGame()

    def doBoardMove(self,boardMove: BoardMoves) -> int:
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

    def startGame(self) -> None:
        print(textwrap.dedent(GameText.INTRO.value))

    def triggerLoss(self) -> None:
        # Lose Mechanic
        self.state = GameState.ENDED #inputs for moves no longer register
        print(textwrap.dedent(GameText.LOSE.value))
        
        # Retry Mechanic
        self.printRetryMessage()

    def restartGame(self) -> None:
        """
        Resets:
        1. turn count
        2. score
        3. board (empty board THEN generate new tile THEN print board)
        4. state to PLAYING (keyboard listener back in action)
        5. calculates possiblem oves from new board
        """
        # 1
        self.turnCount = 0
        
        # 2
        self.score.resetScore()

        # 3
        self.board.resetBoard()
        self.board.generateNewTile()
        self.printBoard()

        # 4
        self.state = GameState.PLAYING
        
        # 5
        self.possible_moves = [move for move,legal in self.board.checkPossibleMoves().items() if legal]

    def quitGame(self) -> None:
        self.state = GameState.ENDED
        print(textwrap.dedent(GameText.QUIT.value))
        self.stopKeyboardListener()

    def printBoard(self) -> None:
        print(self.board)
    
    def printScore(self) -> None:
        print(self.score)

    def printRetryMessage(self) -> None:
        print(textwrap.dedent(GameText.RETRY.value))