import numpy as np
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from mctspy.games.examples.connect4 import Connect4GameState

# define inital state
state = np.zeros((7, 7))
board_state = Connect4GameState(
    state=state, next_to_move=np.random.choice([-1, 1]), win=4)

# link pieces to icons
pieces = {0: " ", 1: "X", -1: "O"}

# print a single row of the board
def stringify(row):
    return " " + " | ".join(map(lambda x: pieces[int(x)], row)) + " "

# display the whole board
def display(board):
    board = board.copy().T[::-1]
    for row in board[:-1]:
        print(stringify(row))
        print("-"*(len(row)*4-1))
    print(stringify(board[-1]))
    print()

display(board_state.board)
# keep playing until game terminates
while board_state.game_result is None:
    # calculate best move
    root = TwoPlayersGameMonteCarloTreeSearchNode(state=board_state)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(total_simulation_seconds=1)

    # update board
    board_state = best_node.state
    # display board
    display(board_state.board)

# print result
print(pieces[board_state.game_result])