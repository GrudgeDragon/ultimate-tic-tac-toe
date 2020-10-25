import numpy as np

# returns 1 or -1 if a player won. Returns 0 if draw, return None if game isn't finished.
def winner9(board):
    meta_board = np.array([[None for j in range(3)] for i in range(3)])

    for sub_board_row in range(3):
        row_start = sub_board_row * 3
        for sub_board_col in range(3):
            col_start = sub_board_col * 3
            sub_board = board[row_start:row_start+3, col_start:col_start+3]
            result = winner3(sub_board, 0)
            meta_board[sub_board_row, sub_board_col] = winner3(sub_board, 0)

    return winner3(meta_board, None)


# Finds winner on a 3x3 board
# returns 0 for draw, None for incomplete game
# Note: Algorithm is greedy. If both players have 3 in a row, this function will not take that into account, it will
# report the first win condition it finds.
def winner3(board3, unfinished_key):
    """
    Searches for rows, columns, and diagonals of 1 and -1s

    :param board3: a 3x3 array
    :param unfinished_key: On a t3 board, 0 indicates an unfinished game. On a ut3, a None indicates an unfinished game.
    :return: The winner if one is found (1 or -1). Returns 0 for draw, and None for an unfinished game.
    """
    for i in range(3):
        # check for win in row i
        if board3[i, 0] is not None and board3[i, 0] != 0 and board3[i, 0] == board3[i, 1] and board3[i, 0] == board3[i, 2]:
            return board3[i, 0]

        # check for win in col i
        if board3[i, 0] is not None and board3[0, i] != 0 and board3[0, i] == board3[1, i] and board3[0, i] == board3[2, i]:
            return board3[0, i]

    if board3[i, 0] is not None and board3[0, 0] != 0 and board3[0, 0] == board3[1, 1] and board3[0, 0] == board3[2, 2]:
        return board3[0, 0]

    if board3[i, 0] is not None and board3[2, 0] != 0 and board3[2, 0] == board3[1, 1] and board3[2, 0] == board3[0, 2]:
        return board3[2, 0]

    # No wins, check for draw
    return check_draw(board3, unfinished_key)  # All tiles are filled, return draw


def check_draw(board3, unfinished_key):
    """
    After failing to detect a win condition, use this function to check for draws. This function assumes there are no
    win conditions in the board, and does not check for them.

    :param board3: a 3x3 board that has no wind conditions in it
    :param unfinished_key: On a t3 board, 0 indicates an unfinished game. On a ut3, a None indicates an unfinished game.
    :return: 0 for draw, and None for an unfinished game.
    """

    for r in range(3):
        for c in range(3):
            if board3[r, c] == unfinished_key:  # Moves are left, not a draw
                return None

    return 0  # All tiles are filled, return draw
