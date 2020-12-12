from Game import Game, Red, Yellow, Empty, is_draw, get_winner, GameState
from random import randint, choice

class BotGame(Game):
    """
        Yellow player is human,
        Red player is controlled by computer.
    """

    def bot_place(self, mode="random"):
        if mode == "random":
            super().place(choice(self.state.get_legal_actions()))
        elif mode == "minimax":
            super().place(self.minimax(True, self.state, 5)[0])
        elif mode == "minimax-alphabeta":
            super().place(self.minimax_ab(True, self.state, 6, -float("inf"), float("inf"))[0])
        else:
            raise Exception()

    def minimax_ab(self, maximize, state, depth, alpha, beta):
        actions = state.get_legal_actions()
        
        if depth == 0 or is_terminal(state):
            return (None, evaluate(state))

        if maximize:
            value = -float("inf")
            chosen_action = choice(actions)
            for action in actions:
                successor = state.generate_successor(action)
                new_value = self.minimax_ab(False, successor, depth - 1, alpha, beta)[1]
                if new_value > value:
                    value = new_value
                    chosen_action = action
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (chosen_action, value)
        else:
            value = float("inf")
            chosen_action = choice(actions)
            for action in actions:
                successor = state.generate_successor(action)
                new_value = self.minimax_ab(True, successor, depth - 1, alpha, beta)[1]
                if new_value < value:
                    value = new_value
                    chosen_action = action
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return (chosen_action, value)


    def minimax(self, maximize, state, depth):
        actions = state.get_legal_actions()
        
        if depth == 0 or is_terminal(state):
            return (None, evaluate(state))

        if maximize:
            value = -float("inf")
            chosen_action = choice(actions)
            for action in actions:
                successor = state.generate_successor(action)
                new_value = self.minimax(False, successor, depth - 1)[1]
                if new_value > value:
                    value = new_value
                    chosen_action = action
            return (chosen_action, value)
        else:
            value = float("inf")
            chosen_action = choice(actions)
            for action in actions:
                successor = state.generate_successor(action)
                new_value = self.minimax(True, successor, depth - 1)[1]
                if new_value < value:
                    value = new_value
                    chosen_action = action
            return (chosen_action, value)


def is_terminal(state):
    return get_winner(state) != None or is_draw(state)

def evaluate_window(window, player, negative):
    opponent = Red if player == Yellow else Yellow
    if window.count(opponent) > 0:
        return 0

    scores = ( float("inf"), 15, 6, 2, 0 )
    stones_needed = window.count(Empty)
    score = scores[stones_needed]
    return -0.5 * score if negative else score
        

def evaluate(state):
    player = state._current_player
    board = state._board
    if get_winner(state) == player:
        return float("inf")
    elif get_winner(state) != None:
        return -float("inf")
    elif is_draw(state):
        return 0
    
    score = 0
    # Middle bias during the first 6 turns
    values = (0, 0, 3, 5, 3, 0, 0)
    if state.turns < 6:
        for x in range(state.width):
            for y in range(state.height):
                if board[x][y] == player:
                    score += values[x]

    # diagonal window starting positions (positive/negative slope)
    starts1 = ((0,3), (0,4), (1,3), (0,5), (1,4), (2,3), (1,5), (2,4), (3,3), (2,5), (3,4), (3,5))
    starts2 = ( (6 - start[0], start[1]) for start in starts1)

    for eval_player in (Red, Yellow):

        # Check diagonally
        for direction in ((1,-1,starts1), (-1,-1,starts2)):
            dx = direction[0]
            dy = direction[1]
            starts = direction[2]
            for start in starts:
                window = []
                for i in range(4):
                    x = start[0]+ dx * i
                    y = start[1] + dy * i
                    window.append(board[x][y])
                score += evaluate_window(window, eval_player, eval_player != player)

        # Check horizontally
        for y in range(state.height):
            row = [ board[x][y] for x in range(state.width)]
            for x in range(state.width - 3):
                window = row[x:x+4]
                score += evaluate_window(window, eval_player, eval_player != player)

        # Check vertically
        for x in range(state.width):
            col = board[x]
            for y in range(state.height - 3):
                window = col[y:y+4]
                score += evaluate_window(window, eval_player, eval_player != player)


    return score


if __name__ == "__main__":
    state = GameState()
    state = state.generate_successor(0)
    state = state.generate_successor(1)
    state = state.generate_successor(0)
    state = state.generate_successor(2)
    print(evaluate(state))