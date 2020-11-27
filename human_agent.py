import ut3_game
from board_utils import *

class HumanAgent(ut3_game.UT3Agent):

    def __init__(self, name):
        super().__init__(name)
        self.next_move = None

    def make_move(self, global_board, local_board_index):
        return self.next_move