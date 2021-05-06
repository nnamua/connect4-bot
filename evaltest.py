from game import Game
from algorithms import evaluate

"""
    Starts a game in the console.
    Both player actions are controlled by the user.
    Prints the score of the evaluation function for each game state.
"""

if __name__ == "__main__":

    print("Starting game...")
    g = Game()

    while not g.state.isTerminal():
        print(f"Current player: {g.state.currentPlayer}")
        print(f"Evaluation score for current player: {evaluate(g.state)}")
        print(g.state.board)
        actions = g.state.getLegalActions()
        print(f"Possible actions: {actions}")

        action = -1
        while action not in actions:
            action = input("Please select one of these actions:     ")
            try:
                action = int(action)
            except:
                print("Please enter an integer.")

        g.place(action)