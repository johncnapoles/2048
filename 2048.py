from gamelogic import GameLogic

def main():
    try:    
        game = GameLogic()
        game.startGame()
        game.startKeyboardListener()
    except KeyboardInterrupt:
        # Ignores attempt to stop program by inputting ctrl+c
        pass

if __name__ == "__main__":
    main()