import ut3_game
from board_utils import *

def get_replay_agents_from_file(file_name):
    json_data = get_json_from_log(file_name)
    moves = get_moves_from_json(json_data)
    agent1_moves = [moves[i] for i in range(0, len(moves), 2)]
    agent2_moves = [moves[i] for i in range(1, len(moves), 2)]

    agent1_name = "{}_from_{}".format(json_data["players"][0], file_name)
    agent2_name = "{}_from_{}".format(json_data["players"][1], file_name)

    return ReplayAgent(agent1_name, agent1_moves), ReplayAgent(agent2_name, agent2_moves)

class ReplayAgent(ut3_game.UT3Agent):

    def __init__(self, name, moves):
        super().__init__(name)
        self.moves = moves
        self.move_num = 0

    def make_move(self, global_board, local_board_index):
        move = self.moves[self.move_num]
        self.move_num += 1
        return move