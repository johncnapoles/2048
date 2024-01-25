from enum import Enum
from pynput import keyboard

class Tile(Enum):
    TWO = 2
    FOUR = 4
    EIGHT = 8
    ONESIX = 16
    THREERWO = 32
    SIXFOUR = 64
    ONETWOEIGHT = 128
    TWOFIVESIX = 256
    FIVEONETWO = 512
    ONEOHTWOFOUR = 1024
    TWOOHFOUREIGHT = 2048

class Actions(Enum):
    UP = keyboard.Key.up
    DOWN = keyboard.Key.down
    LEFT = keyboard.Key.left
    RIGHT = keyboard.Key.right
    ESCAPE = keyboard.Key.esc

class BoardMoves(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
class GameState(Enum):
    START_SCREEN = "START_SCREEN"
    PLAYING = "PLAYING"
    ENDED = "ENDED"

class GameText(Enum):
    INTRO = """
        Welcome to 2048.
        Press <ESC> to quit the game at anytime
        Press <UP,DOWN,LEFT,RIGHT> key to start...
        """
    QUIT = """
        Exiting game. Goodbye!
        """
    LOSE = """
        You died
        """