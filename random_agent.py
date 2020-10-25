import random as rand
import board_utils

class RandomAgent:

    #
    #   player: 1 or -1
    def __init__(self, player):
        self.player = player

    # The agent makes a move
    #   board: is 9x9 board state
    #   local_board: if not null, a tuple representing the sub_board that must be used ([0-2],[0-2])
    def make_move(self, global_board, local_board_index):

        # if local_board is given
        if local_board_index is not None:
            # Validate it
            if local_board_index[0] < 0 or local_board_index[0] > 2 or local_board_index[1] < 0 or local_board_index[1] > 2:
                print("Bad local_board_index")
                return None
            row_start = local_board_index[0] * 3
            col_start = local_board_index[1] * 3
            # TODO: If the forced board is completed, skip. This probably shouldn't happen though
            return self.random_local_board_move(global_board, row_start, col_start)

        # if local_board isn't set, choose one at random
        local_board_list = [i for i in range(9)]
        rand.shuffle(local_board_list)

        # Try each local_board until a valid move is found
        for i in range(9):
            local_board = local_board_list[i]
            row_start = (local_board // 3) * 3
            col_start = (local_board % 3) * 3
            # TODO: If this board has a win condition, skip
            move = self.random_local_board_move(global_board, row_start, col_start)
            if move is not None:
                return move
        else:
            print("Random agent couldn't find a valid move")

    def random_local_board_move(self, board, row_start, col_start):
        # Get a random list of moves
        move_list = [i for i in range(9)]
        rand.shuffle(move_list)

        # Try each move until a valid one is found
        final_move = None
        for i in range(9):
            move = move_list[i]
            row = move // 3 + row_start
            col = move % 3 + col_start
            if board[row, col] == 0:
                final_move = (row, col)
                break

        return final_move
