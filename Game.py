from discord.utils import _string_width
from copy import deepcopy


Red = "red"
Yellow = "yellow"
Empty = None

def is_draw(state):
    return state.turns == state.width * state.height

def get_winner(state):
    # Check for vertical wins
    for x in range(state.width):
        score = 0
        last_stone = None
        for y in range(state.height):
            stone = state._board[x][y]
            if stone != last_stone:
                score = 1
                last_stone = stone
            elif stone != Empty:
                score += 1
                if score >= 4:
                    return stone

    # Check for horizontal wins
    for y in range(state.height):
        score = 0
        last_stone = None
        for x in range(state.width):
            stone = state._board[x][y]
            if stone != last_stone:
                score = 1
                last_stone = stone
            elif stone != Empty:
                score += 1
                if score >= 4:
                    return stone

    # Check for diagonal wins (two different diagonal possibilities)
    # (1,1,0) -> (delta_x, delta_y, startx when iterating y)
    for direction in ((1, 1,0), (-1,1,state.width-1)):
        for startx in range(state.width):
            y = 0
            x = startx
            score = 0
            last_stone = None
            while x >= 0 and x < state.width and y >= 0 and y < state.height:
                stone = state._board[x][y]
                if stone != last_stone:
                    score = 1
                    last_stone = stone
                elif stone != Empty:
                    score += 1
                    if score >= 4:
                        return stone

                x += direction[0]
                y += direction[1]

        for starty in range(state.height):
            y = starty
            x = direction[2]
            score = 0
            last_stone = None
            while x >= 0 and x < state.width and y >= 0 and y < state.height:
                stone = state._board[x][y]
                if stone != last_stone:
                    score = 1
                    last_stone = stone
                elif stone != Empty:
                    score += 1
                    if score >= 4:
                        return stone

                x += direction[0]
                y += direction[1]

    return None

class GameState:
    def __init__(self, width=7, height=6):
        self._board = []
        self.width = width
        self.height = height
        self._current_player = Yellow
        self.turns = 0
        
        # Generate the starting board
        for x in range(width):
            col = []
            for y in range(height):
                col.append(Empty)
            self._board.append(col)

    def get_legal_actions(self):
        possible = []
        for x in range(self.width):
            col = self._board[x]
            if col.count(Empty) > 0:
                possible.append(x)
        return possible

    def generate_successor(self, col_nr):
        successor = GameState(width=self.width, height=self.height)
        successor._board = deepcopy(self._board)
        successor._current_player = self._current_player

        col_ok = successor._place(col_nr)
        return successor if col_ok else None

    def count(self, stone):
        n = 0
        for x in range(self.width):
            for y in range(self.height):
                if self._board[x][y] == stone:
                    n += 1

        return n

    def _next_player(self):
        self._current_player = Red if self._current_player == Yellow else Yellow

    def _place(self, col_nr):
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


class Game:
    def __init__(self):
        self.state = GameState()
        
        self.red_player = None
        self.yellow_player = None
        self.message = None
        self.channel = None
        self.winner = None
        self.turns = 0

    def get_height(self):
        return self.state.height

    def get_width(self):
        return self.state.width

    def place(self, col_nr):
        successor = self.state.generate_successor(col_nr)
        if successor != None:
            self.state = successor
            return True
        else:
            return False

    def get_player_name(self):
        if self.state._current_player == Red:
            return self.red_player.mention if self.red_player != None else "Red"
        else:
            return self.yellow_player.mention if self.yellow_player != None else "Yellow"

    def check_win(self):
        return get_winner(self.state) != None

    def check_draw(self):
        return is_draw(self.state)

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
        return self.state._board[x][y] == Red

    def is_yellow(self, x, y):
        return self.state._board[x][y] == Yellow

    def is_empty(self, x, y):
        return self.state._board[x][y] == Empty

    def is_red_turn(self):
        return self.state._current_player == Red

    def is_yellow_turn(self):
        return self.state._current_player == Yellow

    def get_winner(self):
        winner = get_winner(self.state)
        if self.check_win():
            return self.red_player if winner == Red else self.yellow_player
        else:
            return None

    def get_loser(self):
        winner = get_winner(self.state)
        if self.check_win():
            return self.red_player if winner == Yellow else self.yellow_player
        else:
            return None
    
    def to_dict(self):
        game_dict = dict()
        stone_chars = { Yellow : "y", Red : "r", Empty : "e" }
        board_string = ""
        for x in range(self.state.width):
            for y in range(self.state.height):
                board_string += stone_chars[self.state._board[x][y]]
        game_dict["board"] = board_string
        game_dict["red_player"] = f"#{self.red_player.id}"
        game_dict["yellow_player"] = f"#{self.yellow_player.id}"
        game_dict["winner"] = "" if self.get_winner() == None else f"#{self.get_winner().id}"
        game_dict["turns"] = self.state.turns
        game_dict["width"] = self.state.width
        game_dict["height"] = self.state.height
        return game_dict