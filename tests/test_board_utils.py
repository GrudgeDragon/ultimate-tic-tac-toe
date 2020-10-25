import unittest
import numpy as np
import board_utils


class TestBoardUtils(unittest.TestCase):
    def test_win_conditions_t3(self):
        """
        1 or -1 result is a win by that player
        0 is a draw
        None is an unfinished game
        """
        # Test a t3 board of 0s is unfinished
        board = np.zeros((3, 3))
        self.assertEqual(board_utils.winner3(board, 0), None, "There should be unfinished")

        # Test full board is a draw
        board = np.array([[1, -1, 1],
                          [-1, 1, -1],
                          [-1, 1, -1]])
        self.assertEqual(board_utils.winner3(board, 0), 0, "Game should be a draw")

        # Test unfinished game is unfinished
        board = np.array([[1, -1, 1],
                          [-1, 0, -1],
                          [-1, 1, -1]])
        self.assertEqual(board_utils.winner3(board, 0), None, "Game should be unfinished")

        # Test row
        for i in range(3):
            board[1, i] = 1
        self.assertEqual(board_utils.winner3(board, 0), 1, "Player 1 should win by row")

        # Test col
        board = np.zeros((3, 3))
        for i in range(3):
            board[i, 1] = -1
        self.assertEqual(board_utils.winner3(board, 0), -1, "Player -1 should win by column")

        # Test main diagonal
        board = np.zeros((3, 3))
        for i in range(3):
            board[i, i] = 1
        self.assertEqual(board_utils.winner3(board, 0), 1, "Player 1 should win by diagonal")

        # Test alt diagonal
        board = np.zeros((3, 3))
        for i in range(3):
            board[i, 2-i] = -1
        self.assertEqual(board_utils.winner3(board, 0), -1, "Player -1 should win by diagonal")

    def test_meta_win_condition_t3(self):
        # Test unfinished meta draw is a unfinished, (or draw?)

        # Test a ut3 board of 0s is a draw
        board = np.zeros((3, 3))
        self.assertEqual(board_utils.winner3(board, None), 0, "Game should be draw")

        # Test full board without 3 in a row is a draw
        board = np.array([[1, -1, 1],
                          [-1, 1, -1],
                          [-1, 1, -1]])
        self.assertEqual(board_utils.winner3(board, None), 0, "Game should be a draw")

        # Test unfinished game is unfinished
        board = np.array([[1, -1, 1],
                          [-1, None, -1],
                          [-1, 1, -1]])
        self.assertEqual(board_utils.winner3(board, None), None, "Game should be unfinished")

    def test_no_win(self):
        board = np.zeros((9, 9))
        result = board_utils.winner9(board)
        self.assertEqual(result, None, "The board9 is all 0s, the game should be unfinished")

if __name__ == '__main__':
    unittest.main()
