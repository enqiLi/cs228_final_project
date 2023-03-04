import numpy as np
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from mctspy.games.examples.go import GoGameState

# define inital state
state = np.zeros((7, 7))
board_state = GoGameState(state_matrix=None, board_size=5)

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

def get_board(state):
    return state.state_matrix[0] - state.state_matrix[1]
# display(board_state.board)
display(get_board(board_state))
# keep playing until game terminates
while board_state.game_result is None:
    # calculate best move
    root = TwoPlayersGameMonteCarloTreeSearchNode(state=board_state)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(total_simulation_seconds=1)

    # update board
    board_state = best_node.state
    # display board
    # display(board_state.board)
    display(get_board(board_state))

# print result
print(pieces[board_state.game_result])