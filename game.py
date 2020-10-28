import json
import datetime
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
    # Print game to console, for quick human examination
    print_moves = False

    log_games = True

    # By default, only moves are recorded to keep the logs small. We will want a large number of these logs and:
    # - File IO takes a long time
    # - We're keeping some of these in source control
    # - We can always re-derive the boards from the moves TODO: Add helper for this to board_utils
    log_boards = False

    # Human-readable JSON
    pretty_logs = False

    # If this is set, it will be used for the log name instead of the agent names
    log_prefix = None

    def __init__(self):
        self.agent1 = None
        self.agent2 = None
        self.global_board = np.zeros((9, 9), dtype=int)
        self.next_local_board_index = None
        self.move_number = 0
        self.winner = None
        self.move_list = []
        self.game_data = {}
        self.global_boards = []
        self.meta_boards = []
        self.time = 0
        self.log_name = None

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

        # Print to console
        if self.print_moves:
            self.print_move(move, agent)

        # Logging
        self.move_list.append(move)
        if self.log_boards:
            self.global_boards.append(self.global_board)
            # TODO: Calculate meta_board only once
            self.meta_boards.append(get_meta_board(self.global_board))

        if winner is not None:
            self.end_game(winner, agent)
            return False

        # Determine next local board
        self.next_local_board_index = (move[0] % 3, move[1] % 3)
        next_local_board = get_local_board(self.global_board, self.next_local_board_index)
        if is_player(get_winner_local_board(next_local_board)) or is_board_full(next_local_board, 0):
            self.next_local_board_index = None

        return True

    def play(self, agent1: UT3Agent, agent2: UT3Agent):
        self.__init__()  # Reset most things
        self.agent1: UT3Agent = agent1
        self.agent2: UT3Agent = agent2
        agent1.player_num = 1
        agent2.player_num = -1
        now = datetime.datetime.now()
        self.time = round(now.timestamp() * 1000)  # for log name
        self.game_data["timestamp"] = str(now)  # for log data
        self.game_data["players"] = (agent1.player_name, agent2.player_name)

        # Game loop.
        while self.make_move(self.agent1) and self.make_move(self.agent2):
            pass

        return self.winner

    def end_game(self, winner, agent: UT3Agent):
        self.winner = winner
        if is_player(winner):
            if self.print_moves:
                print("{}({}) won".format(agent.player_name, 'X' if agent.player_num == 1 else 'O'))
        else:
            if self.print_moves:
                print("The game was tied")
        if self.log_games:
            self.game_data["moves"] = self.move_list
            self.game_data["winner"] = agent.player_num
            self.game_data["winner_name"] = agent.player_name
            if self.log_boards:
                # Numpy arrays need to be converted to lists to be serialized in json
                self.game_data["boards"] = [[[int(col) for col in row] for row in board] for board in self.global_boards]
                self.game_data["meta_boards"] = [[[int(col) if col is not None else None for col in row] for row in board] for board in self.meta_boards]

            log_prefix = self.log_prefix if self.log_prefix is not None \
                else self.agent1.player_name + "_" + self.agent2.player_name
            self.log_name = "logs\\{}_{}".format(log_prefix,
                                            self.time)
                                            #int(round(self.game_time.microsecond * 1000)))
            with open(self.log_name, 'w') as outfile:
                json.dump(self.game_data, outfile, indent=4 if self.pretty_logs else None)

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
        # TODO: Implement this.
        # TODO: Verify with next_local_board.
        # TODO: Verify didn't try to overwrite an existing move
        # TODO: Verify didn't write to a local board that has a winner already
        return move is not None

