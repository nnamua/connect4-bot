from Game import Game, Red, Yellow, Empty
from random import randint, choice

class BotGame(Game):
    """
        Yellow player is human,
        Red player is controlled by computer.
    """

    def bot_place(self):
        possible = []
        for x in range(self.width):
            col = self._board[x]
            if col.count(Empty) > 0:
                possible.append(x)

        super().place(choice(possible))
        
            




    
