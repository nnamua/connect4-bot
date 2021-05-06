from stones import Stone, Red, Yellow, Empty
from state import GameState
import random as rand

# Returns a random actions
def random(state: GameState):
    actions = state.getLegalActions()
    return rand.choice(actions)

# Calculates an optimal action with the minimax algorithm
def minimax(maximize: bool, state: GameState, depth: int):
    actions = state.getLegalActions()
    
    if depth == 0 or state.isTerminal():
        return (None, evaluate(state))

    if maximize:
        value = -float("inf")
        chosenAction = rand.choice(actions)
        for action in actions:
            successor = state.generateSuccessor(action)
            newValue  = minimax(False, successor, depth-1)[1]
            if newValue > value:
                value = newValue
                chosenAction = action
            elif newValue == value: # select randomly if both have same value
                chosenAction = rand.choice((chosenAction, action))
        return (chosenAction, value)
    
    else:
        value = float("inf")
        chosenAction = rand.choice(actions)
        for action in actions:
            successor = state.generateSuccessor(action)
            newValue  = minimax(True, successor, depth-1)[1]
            if newValue < value:
                value = newValue
                chosenAction = action
            elif newValue == value:
                chosenAction = rand.choice((chosenAction, action))
        return (chosenAction, value)

# Calculates an optimal action with the minimax algorithm.
# Optimized with alpha-beta pruning.
def minimaxAB(maximize: bool, state: GameState, depth: int, alpha=-float("inf"), beta=float("inf")):
    actions = state.getLegalActions()

    if depth == 0 or state.isTerminal():
        return (None, evaluate(state))

    if maximize:
        value = -float("inf")
        chosenAction = rand.choice(actions)
        for action in actions:
            successor = state.generateSuccessor(action)
            newValue  = minimaxAB(False, successor, depth - 1, alpha=alpha, beta=beta)[1]
            if newValue > value:
                value = newValue
                chosenAction = action
            elif newValue == value:
                chosenAction = rand.choice((chosenAction, action))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (chosenAction, value)

    else:
        value = float("inf")
        chosenAction = rand.choice(actions)
        for action in actions:
            successor = state.generateSuccessor(action)
            newValue  = minimaxAB(True, successor, depth - 1, alpha=alpha, beta=beta)[1]
            if newValue < value:
                value = newValue
                chosenAction = action
            elif newValue == value:
                chosenAction = rand.choice((chosenAction, action))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (chosenAction, value)

# Evaluates the given states, and returns a score representing
# how good the state is for the current player
def evaluate(state: GameState):
    board    = state.board
    player   = state.currentPlayer
    opponent = Red if player == Yellow else Yellow
    w        = board.width
    h        = board.height

    # Check for wins or draws
    if state.winner() == player:
        return float("inf")
    elif state.winner() != None:
        return -float("inf")
    elif state.isDraw():
        return 0

    score = 0
    # Middle bias
    mid = int(w / 2)
    if w % 2 == 0:
        score += board.column(mid).count(player)
        score -= board.column(mid).count(opponent)
        score += 0.5 * (board.column(mid - 1) + board.column(mid + 1)).count(player)
        score -= 0.5 * (board.column(mid - 1) + board.column(mid + 1)).count(opponent)
    else:
        score += (board.column(mid) + board.column(mid + 1)).count(player)
        score -= (board.column(mid) + board.column(mid + 1)).count(opponent)
        score += 0.5 * (board.column(mid - 1) + board.column(mid + 2)).count(player)
        score -= 0.5 * (board.column(mid - 1) + board.column(mid + 2)).count(opponent)
    
    # Horizontal: Loop through all 4-blocks, add/subtract a score of 5 if a player
    # has 3 consecutive stones in this row, with the chance to get a 4th
    for y in range(h):
        blocks = toBlocks(board.row(y))
        rowScore = 0
        for block in blocks:
            rowScore += evaluateBlock(block, player)
        # Allow a maximum score of 5 per row, and a minimum of -5
        score += max(-5, min(5, rowScore))

    # Vertical: Again, loop through all 4-blocks, and add scores
    # similar to the horizontal variant.
    for x in range(w):
        blocks = toBlocks(board.column(x))
        colScore = 0
        for block in blocks:
            colScore += evaluateBlock(block, player)
        score += max(-5, min(5, colScore))

    # Diagonal: Same procedure again.
    # Diagonal window starting positions (LR = left-to-right, RL = right-to-left)
    startsLR = (  (0,2),   (0,1),   (0,0),   (1,0),   (2,0),   (3,0))
    startsRL = ((w-1,2), (w-1,1), (w-1,0), (w-2,0), (w-3,0), (w-4,0))

    slopes = []
    for start in startsLR:
        slope = []
        i = 0
        while (x := start[0] + i) < w and (y := start[1] + i) < h:
            slope.append(board[x][y])
            i += 1
        slopes.append(slope)
    
    for start in startsRL:
        slope = []
        i = 0
        while (x := start[0] - i) >= 0 and (y := start[1] + i) < h:
            slope.append(board[x][y])
            i += 1
        slopes.append(slope)

    for slope in slopes:
        slopeScore = 0
        blocks = toBlocks(slope)
        for block in blocks:
            slopeScore += evaluateBlock(block, player)
        score += max(-5, min(5, slopeScore))

    return score
        
        
# Evaluates a block of 4.
# Returns 5 if player almost has 4, -5 if opponent almost has 4
def evaluateBlock(block, player):
    opponent = Red if player == Yellow else Yellow
    if block.count(player) == 3 and block.count(Empty) == 1:
        return 5
    elif block.count(opponent) == 3 and block.count(Empty) == 1:
        return -5
    else:
        return 0

# Splits the givén array into blocks of [blockSize]
def toBlocks(array, blockSize=4):
    if len(array) <= blockSize:
        return (array,)

    blocks = []
    for i in range(0, len(array) - (blockSize - 1)):
        blocks.append(array[i:i+4])
    return tuple(blocks)