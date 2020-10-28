import numpy as np
import json

"""
Terms
t3:           tic-tac-toe
ut3:          ultimate tic-tac-toe
board:        3x3 grid. Can be meta or local.
local_board:  3x3 t3 grid
meta_board:   3x3 ut3 grid that describes the 9 local board win states
global_board: 9x9 ut3 grid

A Note about cat's games:

Cat's games in UT3 are not the same as cat's games in T3. This is because players can place their mark on meta and local
boards consecutively, without their opponent's interference.

For local boards, the game isn't finished until all the spaces
are filled. So the game isn't declared a draw until the local board is full. This is an arbitrary rules choice, but it's
the one we chose. This can be made to be configurable if we like.

For the meta game, you don't have to wait for the meta to fill up, once there's an X and O in every row, column, and
diagonal, the game can be declared a tie because it's un-winnable.

"""
# For local boards
num_to_char = {1: 'X', -1: 'O', 0: ' '}

# For meta boards
num_to_char_meta = {1: 'X', -1: 'O', 0: '*', None: ' '}

def get_local_board(global_board, board_index):
    row_start = board_index[0] * 3
    col_start = board_index[1] * 3
    return global_board[row_start:row_start + 3, col_start:col_start + 3]

def get_meta_board(global_board):
    meta_board = np.array([[None for j in range(3)] for i in range(3)])

    for local_board_row in range(3):
        for local_board_col in range(3):
            local_board = get_local_board(global_board, (local_board_row, local_board_col))
            meta_board[local_board_row, local_board_col] = get_winner_local_board(local_board)
    return meta_board

def get_global_winner(global_board):
    """
    Checks for a win condition in the global board.

    :param global_board:
    :return:  1 or -1 if a player won.
              0 if board is full, or more likely, the global_board is un-winnable,
              None if game isn't finished.
    """
    meta_board = get_meta_board(global_board)

    result = get_winner_meta_board(meta_board)

    # If no one's won the meta yet, check for cat's game
    if result is None and not is_board_winnable(meta_board, is_meta=True):
        return 0

    return result

def get_winner_local_board(board):
    return get_winner_board(board, unfinished_key=0)


def get_winner_meta_board(board):
    return get_winner_board(board, unfinished_key=None)


def is_player(value):
    return value == 1 or value == -1

# Finds winner on a 3x3 board
# returns 0 for draw, None for incomplete game
# Note: Algorithm is greedy. If both players have 3 in a row, this function will not take that into account, it will
# report the first win condition it finds.
def get_winner_board(board, unfinished_key):
    """
    Searches for rows, columns, and diagonals of 1 and -1s

    :param board: a 3x3 array
    :param unfinished_key: On a T3 board, 0 indicates an unfinished game. On a UT3, a None indicates an unfinished game.
    :return: The winner if one is found (1 or -1). Returns 0 for full board, and None for an unfinished game.
    """
    for i in range(3):
        # check for win in row i
        if is_player(board[i, 0]) and board[i, 0] == board[i, 1] and board[i, 0] == board[i, 2]:
            return board[i, 0]

        # check for win in col i
        if is_player(board[0, i]) and board[0, i] == board[1, i] and board[0, i] == board[2, i]:
            return board[0, i]

    if is_player(board[0, 0]) and board[0, 0] == board[1, 1] and board[0, 0] == board[2, 2]:
        return board[0, 0]

    if is_player(board[2, 0]) and board[2, 0] == board[1, 1] and board[2, 0] == board[0, 2]:
        return board[2, 0]

    # No wins, check for draw caused by full board
    if is_board_full(board, unfinished_key):
        return 0
    else:
        return None


def is_board_full(board, unfinished_key):
    """
    After failing to detect a win condition, use this function to check for full boards. This function assumes there are
    no win conditions in the board, and does not check for them. This won't catch all cats' games, just games that
    cannot continue because the board is full.

    :param board: a 3x3 board that has no wind conditions in it
    :param unfinished_key: On a T3 board, 0 indicates an unfinished game. On a UT3, a None indicates an unfinished game.
    :return: 0 for draw, and None for an unfinished game.
    """

    for r in range(3):
        for c in range(3):
            if board[r, c] == unfinished_key:  # Moves are left, not a draw
                return False

    return True  # All tiles are filled, return draw

def is_board_winnable(board, is_meta):
    """
    After checking for win conditions, you can check if a board is a cats game. This function doesn't check for win
    conditions first. It will greedily look for the first row without both players in it, so a board with a win in it
    will always be considered a winnable game by this algorithm. If you don't like it, add a new function without the
    greedy suffix.

    Note: This algorithm doesn't make sense for normal T3. This is because one player can make several moves in a row in
    a local or global board without being blocked by the other player.

    Example of a board that would be a cat's game in normal T3, but isn't a cat's game in UT3
    X|O|X
     |X|
    O|X|O

    :param board: 3x3 array that doesn't contain a win condition
    :return: true if the game cannot be won by either player.
    """

    # Check rows
    for row in range(3):
        player1_in_row = False
        player2_in_row = False
        draw_in_row = False
        for col in range(3):
            if board[row, col] == 1:
                player1_in_row = True
            elif board[row, col] == -1:
                player2_in_row = True
            elif board[row, col] == 0 and is_meta:
                draw_in_row = True
        # Still winnable if we didn't see both players.
        if not (player1_in_row and player2_in_row) and not draw_in_row:
            return True

    # Check columns
    for col in range(3):
        player1_in_col = False
        player2_in_col = False
        draw_in_col = False
        for row in range(3):
            if board[row, col] == 1:
                player1_in_col = True
            elif board[row, col] == -1:
                player2_in_col = True
            elif board[row, col] == 0 and is_meta:
                draw_in_col = True

        # Still winnable if we didn't see both players.
        if not (player1_in_col and player2_in_col) and not draw_in_col:
            return True

    # Check main diagonal
    player1_in_diagonal = False
    player2_in_diagonal = False
    draw_in_diagonal = False
    for i in range(3):
        if board[i, i] == 1:
            player1_in_diagonal = True
        elif board[i, i] == -1:
            player2_in_diagonal = True
        elif board[i, i] == 0 and is_meta:
            draw_in_diagonal = True
    if not (player1_in_diagonal and player2_in_diagonal) and not draw_in_diagonal:
        return True

    # Check second diagonal
    player1_in_diagonal = False
    player2_in_diagonal = False
    draw_in_diagonal = False
    for i in range(3):
        if board[i, 2-i] == 1:
            player1_in_diagonal = True
        elif board[i, 2-i] == -1:
            player2_in_diagonal = True
        elif board[i, 2-i] == 0 and is_meta:
            draw_in_diagonal = True
    if not (player1_in_diagonal and player2_in_diagonal) and not draw_in_diagonal:
        return True

    # Could not find a row with both players in it, is still winnable.
    return False

def print_global_board(global_board):
    letter_board = [[num_to_char[player] for player in row] for row in global_board]
    print("  0 1 2  3 4 5  6 7 8")
    for row in range(9):
        if (row % 3 == 0 and row != 0):
            print("  " + "-"*20)

        print(str(row) + " ", end="")

        for col3 in range(3):
            for col in range(3):
                print(letter_board[row][col3*3+col] + " ", end="")
            print("|" if col3 != 2 else "", end="")
        print()

def print_board(board):
    letter_board = [[num_to_char_meta[num] for num in row] for row in board]
    for row in range(3):
        if row != 0:
            print("-"*9)
        for col in range(3):
            print(letter_board[row][col], end="")
            print(" | " if col != 2 else "", end="")
        print()

# Get json from log file, without processing
def get_json_from_log(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def get_moves_from_json(json_data):
    return [(m[0], m[1])for m in json_data["moves"]]

def get_data_from_log(file_name):
    json_data = get_json_from_log(file_name)
    moves = get_moves_from_json(json_data)
    if "boards" in json_data:
        boards = [np.array(board) for board in json_data["boards"]]
        meta_boards = [np.array(board) for board in json_data["meta_boards"]]
    else:
        # Generate boards
        global_board = np.zeros((9, 9), dtype=int)
        boards = []
        player = 1
        meta_boards = []
        for move in moves:
            global_board[move] = player
            player = -player
            boards.append(global_board)
            meta_boards.append(get_meta_board(global_board))
    return moves, boards, meta_boards