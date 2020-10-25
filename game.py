import numpy as np
from board_utils import *


class UT3Agent:
    def __init__(self, player_name):
        self.player_num = None
        self.player_name = player_name

    def make_move(self, global_board, local_board_index):
        return (0, 0)


"""
The game should never give a bad board constraint
"""

class UT3Game:
    print_moves = True

    def __init__(self):
        self.agent1 = None
        self.agent2 = None
        self.global_board = np.zeros((9, 9), dtype=int)
        self.next_local_board_index = None
        self.move_number = 0
        self.winner = None

    def make_move(self, agent: UT3Agent):
        # make move
        self.move_number += 1
        move = agent.make_move(self.global_board, self.next_local_board_index)
        # validate
        if not self.validate_move(self.global_board, self.next_local_board_index, move):
            # TODO: Handle bad moves
            print("{} was an invalid move".format(move))
            return False


        # apply to board
        self.global_board[move] = agent.player_num
        # check for win condition
        winner = get_global_winner(self.global_board)

        if self.print_moves:
            self.print_move(move, agent)

        if winner is not None:
            self.winner = winner
            if is_player(winner):
                if self.print_moves:
                    print("{}({}) won".format(agent.player_name, 'X' if agent.player_num == 1 else 'O'))
                return False
            else:
                if self.print_moves:
                    print("The game was tied")
                return False

        self.next_local_board_index = (move[0] % 3, move[1] % 3)
        next_local_board = get_local_board(self.global_board, self.next_local_board_index)
        if is_player(get_winner_local_board(next_local_board)) or is_board_full(next_local_board, 0):
            self.next_local_board_index = None

        return True

    def play(self, agent1, agent2):
        self.agent1 = agent1
        self.agent2 = agent2
        agent1.player_num = 1
        agent2.player_num = -1

        # Game loop.
        while self.make_move(self.agent1) and self.make_move(self.agent2):
            pass

        return self.winner

    def print_move(self, last_move, agent: UT3Agent):
        print("Move", self.move_number)
        print("{} to {}".format(num_to_char[agent.player_num], last_move))
        print("Board:")
        print_global_board(self.global_board)
        print("Meta-board:")
        print_board(get_meta_board(self.global_board))
        print()
        print()

    # validate_move
    # Checks that an agent placed a move in
    #   move: is a tuple that corresponds to a position on the board.
    def validate_move(self, global_board, next_local_board, move):
        return move is not None

