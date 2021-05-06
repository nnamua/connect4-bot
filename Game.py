from stones import Stone, Red, Yellow, Empty
from state import GameState, IllegalActionException
from algorithms import random, minimax, minimaxAB

class Game:
    def __init__(self):
        self.state = GameState()

        # Initialize discord data
        self.redPlayer    = None
        self.yellowPlayer = None
        self.message      = None
        self.channel      = None
        self.winner       = None

    # Returns the height of the board
    def height(self):
        return self.state.board.height

    # Returns the width of the board
    def width(self):
        return self.state.board.width

    # Places a stone on the board
    def place(self, action: int):
        try:
            successor = self.state.generateSuccessor(action)
        except IllegalActionException:
            return False

        self.state = successor
        return True

    # Returns true if current player is Yellow
    def isYellowTurn(self):
        return self.state.currentPlayer == Yellow

    # Returns true if current player is Red
    def isRedTurn(self):
        return self.state.currentPlayer == Red

    # Returns true if the discord user is the current player
    # Will set the player for red, if unitialized
    def isUserTurn(self, user: Stone):
        if self.isYellowTurn() and self.yellowPlayer == user:
            return True
        else:
            if self.redPlayer == None:
                self.redPlayer = user
                return True
            else:
                return self.redPlayer == user

    # Returns the mention of the current player
    def currentPlayerString(self):
        if self.state.currentPlayer == Red:
            return self.redPlayer.mention if self.redPlayer != None else "Red"
        else:
            return self.yellowPlayer.mention if self.yellowPlayer != None else "Yellow"

    # Returns the winning discord user (None if no winner)
    def getWinner(self):
        winner = self.state.winner()
        if winner == Red:
            return self.redPlayer
        elif winner == Yellow:
            return self.yellowPlayer
        else:
            return None

    # Returns the losing discord user (None if no winner)
    def getLoser(self):
        winner = self.state.winner()
        if winner == Red:
            return self.yellowPlayer
        elif winner == Yellow:
            return self.redPlayer
        else:
            return None

    # Returns the object as a dictionary
    def toDict(self):
        gameDict = dict()
        boardString = [ stone for stone in self.state.board.flatten() ]
        gameDict["board"] = boardString
        gameDict["redPlayer"] = f"#{self.redPlayer.id}"
        gameDict["yellowPlayer"] = f"#{self.yellowPlayer.id}"
        gameDict["winner"] = "" if self.getWinner() == None else f"#{self.getWinner().id}"
        gameDict["turns"] = self.state.turns
        gameDict["width"] = self.state.board.width
        gameDict["height"] = self.state.board.height
        return gameDict
        
# BotGame modes
RANDOM     = "RANDOM"
MINIMAX    = "MINIMAX"
MINIMAX_AB = "MINIMAX_AB"

class BotGame(Game):

    def __init__(self, mode=RANDOM, depth=4):
        self.mode = mode
        self.depth = depth

    # Represents a move by the computer
    def botPlace(self):
        #print(f"Calculating move using mode={self.mode} with a depth of {self.depth}.")

        if self.mode == MINIMAX:
            super().place(minimax(True, self.state, self.depth)[0])

        elif self.mode == MINIMAX_AB:
            super().place(minimaxAB(True, self.state, self.depth)[0])

        else:
            super().place(random(self.state))