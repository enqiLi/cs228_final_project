import numpy as np
from mctspy.games.common import TwoPlayersAbstractGameState, AbstractGameAction
from mctspy.games.examples import gogame


class GoMove(AbstractGameAction):
    def __init__(self, x_coordinate, y_coordinate):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        # self.value = value
        # self.is_pass = False

    def __repr__(self):
        # if self.is_pass:
        #     return "Pass"
        # else:
        return "x:{0} y:{1}".format(
            self.x_coordinate,
            self.y_coordinate,
        )


class GoGameState(TwoPlayersAbstractGameState):

    def __init__(self, state_matrix, board_size, next_to_move=0):
        self.board_size = board_size
        if state_matrix is None:
            self.state_matrix = gogame.init_state(self.board_size)
        else:
            self.state_matrix = state_matrix
        self.next_to_move = next_to_move
        

    @property
    def game_result(self):
        if self.is_game_over():
            return gogame.winning(self.state_matrix)

        # if not over - no result
        return None

    def is_game_over(self):
        return gogame.game_ended(self.state_matrix)

    # def is_move_legal(self, move):
    #     # check if correct player moves
    #     if move.value != self.next_to_move:
    #         return False

    #     # check if inside the board on x-axis
    #     x_in_range = (0 <= move.x_coordinate < self.board_size)
    #     if not x_in_range:
    #         return False

    #     # check if inside the board on y-axis
    #     y_in_range = (0 <= move.y_coordinate < self.board_size)
    #     if not y_in_range:
    #         return False

    #     # finally check if board field not occupied ye
    #     return self.board[move.x_coordinate, move.y_coordinate] == 0

    def move(self, move):
        if isinstance(move, GoMove):
            assert 0 <= move.x_coordinate <= self.board_size
            assert 0 <= move.y_coordinate < self.board_size
            action = self.board_size * move.x_coordinate + move.y_coordinate
        elif move is None:
            action = self.board_size ** 2
        next_state_matrix = gogame.next_state(self.state_matrix, action, canonical=False)
        # print("The next state matrix has {}".format(next_state_matrix.shape))
        next_to_move = gogame.turn(next_state_matrix) + 1
        if next_to_move == 2:
            next_to_move -= 3
        return type(self)(next_state_matrix, self.board_size, next_to_move)

    def get_legal_actions(self):
        # indices = np.where(self.board == 0)
        # return [
        #     TicTacToeMove(coords[0], coords[1], self.next_to_move)
        #     for coords in list(zip(indices[0], indices[1]))
        # ]
        valid_move_idcs = np.argwhere(self.valid_moves()).flatten()
        legalactions = [GoMove(m // self.board_size, m % self.board_size) for m in valid_move_idcs]
        # print(legalactions)
        return legalactions
    
    def invalid_actions(self):
        return gogame.invalid_moves(self.state_matrix)

    def valid_moves(self):
        return 1 - self.invalid_actions()
