import unittest

import numpy as np

import random_agent


class TestRandomAgent(unittest.TestCase):

    agent = random_agent.RandomAgent(1)

    # Test range of moves that random moves are in range.
    def test_range(self):
        board = np.zeros((9, 9))
        for i in range(100):
            move = self.agent.make_move(board, None)
            self.assertTrue(move is not None)
            self.assertIn(move[0], range(0, 9), "Row must be in valid range")
            self.assertIn(move[1], range(0, 9), "Col must be in valid range")

    # Test constraining the set of moves an agent can make.
    def test_constraint(self):
        board = np.zeros((9, 9))

        # Test upper left quadrant
        for i in range(20):
            (row, col) = self.agent.make_move(board, (0, 0))
            self.assertIn(row, range(0, 3), "Row must be in valid range")
            self.assertIn(col, range(0, 3), "Col must be in valid range")

        # test middle quadrant
        for i in range(20):
            (row, col) = self.agent.make_move(board, (1, 1))
            self.assertIn(row, range(3, 6), "Row must be in valid range")
            self.assertIn(col, range(3, 6), "Col must be in valid range")

        # test bottom left quadrant
        for i in range(20):
            (row, col) = self.agent.make_move(board, (2, 0))
            self.assertIn(row, range(6, 9), "Row must be in valid range")
            self.assertIn(col, range(0, 3), "Col must be in valid range")

        # test bottom right quadrant
        for i in range(20):
            (row, col) = self.agent.make_move(board, (2, 2))
            self.assertIn(row, range(6, 9), "Row must be in valid range")
            self.assertIn(col, range(6, 9), "Col must be in valid range")

    def test_can_make_move_on_dense_board(self):
        # Make a board with only a few valid moves left
        board = np.ones((9, 9))
        for i in range(3):
            board[3 + i, 4] = 0
            board[4, 3 + i] = 0

        for i in range(100):
            move = self.agent.make_move(board, None)
            self.assertIn(move[0], range(3, 6), "Move must be the only valid one left on board")
            self.assertIn(move[1], range(3, 6), "Move must be the only valid one left on board")

    def test_dont_write_to_completed_subboards(self):
        print("\nSkipping test_dont_write_to_completed_subboards")
        #return
        board = np.zeros((9, 9))
        for i in range(9):
            board[0, i] = 1  # Complete top 3 subboards
            board[i, 0] = 1  # Complete left 3 subboards
            board[i, i] = 1  # Complete a diagonal of subboards

        for i in range(3):
            board[3 + i, 8 - i] = 1  # Complete second to last subboard with a descending diagonal

        # Test that all moves occur in the bottom center subboard
        for i in range(20):
            (row, col) = self.agent.make_move(board, None)
            # TODO: IMPLEMENT
            self.assertIn(row, range(6, 9), "Must choose a row in the only available local board")
            self.assertIn(col, range(3, 6), "Must choose a column in the only available local board")



if __name__ == '__main__':
    unittest.main()
