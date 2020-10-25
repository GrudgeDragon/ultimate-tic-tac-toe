import unittest
import numpy as np
import board_utils

unwinnable_boards = [np.array([[1, -1, -1],
                               [-1,  1,  1],
                               [ 0,  1, -1]])]

winnable_boards = [np.array([[1, -1, 0],
                             [-1,  1,  1],
                             [ 0,  1, -1]]),
                   np.array([[ 1, -1,  1],
                            [ 1,  0,  1],
                            [ 0, -1, -1]])]

class TestBoardUtils(unittest.TestCase):
    def test_win_condition(self):
        # Test win in the top row.
        board = np.zeros((9, 9))
        for i in range(9):
            board[0, i] = 1
        self.assertEqual(board_utils.get_global_winner(board), 1, "Player 1 should win")

        # Test win in the first column.
        board = np.zeros((9, 9))
        for i in range(9):
            board[i, 0] = -1
        self.assertEqual(board_utils.get_global_winner(board), -1, "Player -1 should win")

    def test_win_condition_no_winner(self):

        # Empty board is unfinished.
        board = np.zeros((9, 9))
        result = board_utils.get_global_winner(board)
        self.assertEqual(result, None, "The board9 is all 0s, the game should be unfinished")

    def test_win_subboard_t3(self):
        """
        return values
        1 or -1 result is a win by that player
        0 is a draw
        None is an unfinished game

        For these tests we pass 0 as the unfinished_key because a 0 on the board indicates an unfinished game of
        normal tic-tac-toe
        """
        # Test a t3 board of 0s is unfinished.
        board = np.zeros((3, 3))
        self.assertEqual(board_utils.get_winner_local_board(board), None, "There should be unfinished")

        # Test full board is a draw.
        board = np.array([[1, -1, 1],
                          [-1, 1, -1],
                          [-1, 1, -1]])
        self.assertEqual(board_utils.get_winner_local_board(board), 0, "Game should be a draw")

        # Test unfinished game is unfinished.
        board = np.array([[1, -1, 1],
                          [-1, 0, -1],
                          [-1, 1, -1]])
        self.assertEqual(board_utils.get_winner_local_board(board), None, "Game should be unfinished")

        # Test row.
        for i in range(3):
            board[1, i] = 1
        self.assertEqual(board_utils.get_winner_local_board(board), 1, "Player 1 should win by row")

        # Test col.
        board = np.zeros((3, 3))
        for i in range(3):
            board[i, 1] = -1
        self.assertEqual(board_utils.get_winner_local_board(board), -1, "Player -1 should win by column")

        # Test main diagonal.
        board = np.zeros((3, 3))
        for i in range(3):
            board[i, i] = 1
        self.assertEqual(board_utils.get_winner_local_board(board), 1, "Player 1 should win by diagonal")

        # Test alt diagonal.
        board = np.zeros((3, 3))
        for i in range(3):
            board[i, 2-i] = -1
        self.assertEqual(board_utils.get_winner_local_board(board), -1, "Player -1 should win by diagonal")

    def test_win_condition_ut3(self):
        """
        1 or -1 result is a win by that player
        0 is a draw
        None is an unfinished game

        For these tests we pass None as the unfinished_key because a None on the board indicates an unfinished game of
        meta tic-tac-toe
        """
        # TODO: Test unfinished meta draw is a unfinished, (or draw?).
        print("\nMissing test for behavior around meta-cats game")

        # Test a ut3 board of 0s is a draw.
        board = np.zeros((3, 3))
        self.assertEqual(board_utils.get_winner_meta_board(board), 0, "Game should be draw")

        # Test full board without 3 in a row is a draw.
        board = np.array([[1, -1, 1],
                          [-1, 1, -1],
                          [-1, 1, -1]])
        self.assertEqual(board_utils.get_winner_meta_board(board), 0, "Game should be a draw")

        # Test unfinished game is unfinished.
        board = np.array([[1, -1, 1],
                          [-1, None, -1],
                          [-1, 1, -1]])
        self.assertEqual(board_utils.get_winner_meta_board(board), None, "Game should be unfinished")

    def test_winnable_games(self):
        for board in unwinnable_boards:
            self.assertFalse(board_utils.is_board_winnable(board), "This should be an unwinnable game")

        for board in winnable_boards:
            self.assertTrue(board_utils.is_board_winnable(board), "This should be a winnable game")

if __name__ == '__main__':
    unittest.main()
