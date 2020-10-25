import random as rand

class RandomAgent:

    #
    #   player: 1 or -1
    def __init__(self, player):
        self.player = player

    # The agent makes a move
    #   board: is 9x9 board state
    #   sub_board: if not null, a tuple representing the sub_board that must be used ([0-2],[0-2])
    def make_move(self, board, subboard_index):

        # if subboard is given
        if subboard_index is not None:
            # Validate it
            if subboard_index[0] < 0 or subboard_index[0] > 2 or subboard_index[1] < 0 or subboard_index[1] > 2:
                print("Bad subboard_index")
                return None
            row_start = subboard_index[0] * 3
            col_start = subboard_index[1] * 3
            return self.random_subboard_move(board, row_start, col_start)

        # if subboard isn't set, choose one at random
        subboard_list = [i for i in range(9)]
        rand.shuffle(subboard_list)

        # Try each subboard until a valid move is found
        for i in range(9):
            subboard = subboard_list[i]
            row_start = (subboard // 3) * 3
            col_start = (subboard % 3) * 3
            move = self.random_subboard_move(board, row_start, col_start)
            if move is not None:
                return move
        else:
            print("Random agent couldn't find a valid move")

    def random_subboard_move(self, board, row_start, col_start):
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