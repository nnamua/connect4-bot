from stones import Stone, Red, Yellow, Empty
from board import Board

class IllegalActionException(Exception):
    pass

class GameState:
    def __init__(self, width: int=7, height=6):
        self.board = Board(width, height)
        self.currentPlayer = Yellow
        self.turns = 0

        # Is set by the winner() function, and used for subsequent winner() calls
        # Should only be used after a called to winner()
        self._winner = None

    # Returns true if the action is legal
    def isLegalAction(self, action: int):
        outsideBounds = action < 0 or action >= self.board.width
        col = self.board.column(action)
        return col.count(Empty) > 0 or outsideBounds

    # Returns a tuple of all legal actions
    def getLegalActions(self):
        actions = []
        for x in range(self.board.width):
            if self.isLegalAction(x):
                actions.append(x)

        return tuple(actions)

    # Returns the successor based on the action and current player
    def generateSuccessor(self, action: int):
        if not self.isLegalAction(action):
            raise IllegalActionException()

        successor = GameState(width=self.board.width, height=self.board.height)
        successor.board = self.board.copy()
        successor.currentPlayer = self.currentPlayer
        successor.place(action)
        return successor

    # Returns the number of stones on the board
    def count(self, stone: Stone):
        return self.board.flatten().count(stone)

    # Sets currentPlayer to the next player
    def nextPlayer(self):
        self.currentPlayer = Red if self.currentPlayer == Yellow else Yellow

    # Places a stone of the current player on the board
    def place(self, action: int):
        if not self.isLegalAction(action):
            raise IllegalActionException()

        column = self.board.column(action)
        for i in range(self.board.height - 1, -1, -1):
            if column[i] == Empty:
                column[i] = self.currentPlayer
                self.turns += 1
                self.nextPlayer()
                return

    # Returns the winner (None if no winner yet / draw)
    def winner(self):
        if self._winner != None:
            return self._winner

        # Check for vertical wins
        for x in range(self.board.width):
            score = 0
            last_stone = None
            for y in range(self.board.height):
                stone = self.board[x][y]
                if stone != last_stone:
                    score = 1
                    last_stone = stone
                elif stone != Empty:
                    score += 1
                    if score >= 4:
                        self._winner = stone
                        return stone

        # Check for horizontal wins
        for y in range(self.board.height):
            score = 0
            last_stone = None
            for x in range(self.board.width):
                stone = self.board[x][y]
                if stone != last_stone:
                    score = 1
                    last_stone = stone
                elif stone != Empty:
                    score += 1
                    if score >= 4:
                        self._winner = stone
                        return stone

        # Check for diagonal wins (two different diagonal possibilities)
        # (1,1,0) -> (delta_x, delta_y, startx when iterating y)
        for direction in ((1, 1,0), (-1,1,self.board.width-1)):
            for startx in range(self.board.width):
                y = 0
                x = startx
                score = 0
                last_stone = None
                while x >= 0 and x < self.board.width and y >= 0 and y < self.board.height:
                    stone = self.board[x][y]
                    if stone != last_stone:
                        score = 1
                        last_stone = stone
                    elif stone != Empty:
                        score += 1
                        if score >= 4:
                            self._winner = stone
                            return stone

                    x += direction[0]
                    y += direction[1]

            for starty in range(self.board.height):
                y = starty
                x = direction[2]
                score = 0
                last_stone = None
                while x >= 0 and x < self.board.width and y >= 0 and y < self.board.height:
                    stone = self.board[x][y]
                    if stone != last_stone:
                        score = 1
                        last_stone = stone
                    elif stone != Empty:
                        score += 1
                        if score >= 4:
                            self._winner = stone
                            return stone

                    x += direction[0]
                    y += direction[1]

        return None

    # Returns true if the game is a draw
    def isDraw(self):
        return self.winner != None and self.turns == self.board.width * self.board.height

    # Returns true if a player has one or if the state is a draw
    def isTerminal(self):
        return (self.winner() != None) or self.isDraw()