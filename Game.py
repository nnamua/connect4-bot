Red = "red"
Yellow = "yellow"
Empty = None

class Game:
    def __init__(self, width=7, height=6):
        self._board = []
        self._current_player = Yellow

        self.width = width
        self.height = height
        self.red_player = None
        self.yellow_player = None
        self.message = None
        self.channel = None
        self.winner = None
        self.turns = 0

        # Generate the starting board
        for x in range(width):
            col = []
            for y in range(height):
                col.append(Empty)
            self._board.append(col)
    
    def _next_player(self):
        self._current_player = Red if self._current_player == Yellow else Yellow

    def get_player(self):
        if self._current_player == Red:
            return self.red_player.mention if self.red_player != None else "Red"
        else:
            return self.yellow_player.mention if self.yellow_player != None else "Yellow"

    def check_draw(self):
        return self.turns == self.width * self.height

    def check_win(self):
        # Check for vertical wins
        for x in range(self.width):
            score = 0
            last_stone = None
            for y in range(self.height):
                stone = self._board[x][y]
                if stone != last_stone:
                    score = 1
                    last_stone = stone
                elif stone != Empty:
                    score += 1
                    if score >= 4:
                        self.winner = stone
                        return True

        # Check for horizontal wins
        for y in range(self.height):
            score = 0
            last_stone = None
            for x in range(self.width):
                stone = self._board[x][y]
                if stone != last_stone:
                    score = 1
                    last_stone = stone
                elif stone != Empty:
                    score += 1
                    if score >= 4:
                        self.winner = stone
                        return True

        # Check for diagonal wins (two different diagonal possibilities)
        # (1,1,0) -> (delta_x, delta_y, startx when iterating y)
        for direction in ((1,1,0), (-1,1,self.width-1)):
            for startx in range(self.width):
                y = 0
                x = startx
                score = 0
                last_stone = None
                while x >= 0 and x < self.width and y >= 0 and y < self.height:
                    stone = self._board[x][y]
                    if stone != last_stone:
                        score = 1
                        last_stone = stone
                    elif stone != Empty:
                        score += 1
                        if score >= 4:
                            self.winner = stone
                            return True
                    x += direction[0]
                    y += direction[1]
                
            for starty in range(self.height):
                y = starty
                x = direction[2]
                score = 0
                last_stone = None
                while x >= 0 and x < self.width and y >= 0 and y < self.height:
                    stone = self._board[x][y]
                    if stone != last_stone:
                        score = 1
                        last_stone = stone
                    elif stone != Empty:
                        score += 1
                        if score >= 4:
                            self.winner = stone
                            return True
                    x += direction[0]
                    y += direction[1]

        return False

    def place(self, col_nr):
        if col_nr < 0 or col_nr >= self.width:
            return False

        col = self._board[col_nr]
        for i in range(self.height - 1, -1, -1):
            if (col[i] == Empty):
                col[i] = self._current_player
                self.turns += 1
                self._next_player()
                return True
        return False

    def is_user_turn(self, user):
        if self.is_yellow_turn() and self.yellow_player == user:
            return True
        elif self.is_red_turn():
            if self.red_player == None:
                self.red_player = user
                return True
            else:
                return self.red_player == user

    def is_red(self, x, y):
        return self._board[x][y] == Red

    def is_yellow(self, x, y):
        return self._board[x][y] == Yellow

    def is_empty(self, x, y):
        return self._board[x][y] == Empty

    def is_red_turn(self):
        return self._current_player == Red

    def is_yellow_turn(self):
        return self._current_player == Yellow

    def get_winner(self):
        return self.red_player if self.winner == Red else self.yellow_player

    def get_loser(self):
        return self.red_player if self.winner == Yellow else self.yellow_player