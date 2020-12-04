import datetime
from board_utils import *
import datetime
from ut3agent import UT3Agent

from board_utils import *

"""
The game should never give a bad board constraint
"""

class UT3Game:
    # Print game to console, for quick human examination
    print_moves = False

    # Save a record of the game
    log_games = True

    # By default, only moves are recorded to keep the logs small.
    log_boards = False

    # Human-readable JSON
    pretty_logs = False

    # If this is set, it will be used for the log name instead of the agent names
    log_prefix = None

    def __init__(self):
        self.agent1 = None
        self.agent2 = None
        self.global_board = np.zeros((9, 9), dtype=int)
        self.directive = None
        self.move_number = 0
        self.winner = None
        self.move_list = []
        self.game_data = {}
        self.global_boards = []
        self.meta_boards = []
        self.time = 0
        self.log_name = None
        self.error = None
        self.last_move = None

    # Returns false when the game ends.
    def make_move(self, agent: UT3Agent):
        """
        Asks the agent to make a move, validates it, and updates the board, checks for win condition.
        :param agent:
        :return: Returns whether or not to continue the game.
        """
        self.move_number += 1
        move = agent.make_move(np.copy(self.global_board), self.directive)

        if not self.validate_move(self.global_board, self.directive, move):
            self.end_game(None, None)
            return False  # End game

        self.global_board[move] = agent.player_num

        # Logging
        if self.print_moves:
            self.print_move(move, agent)
        self.move_list.append(move)
        if self.log_boards:
            self.global_boards.append(self.global_board)
            # TODO: Calculate meta_board only once
            self.meta_boards.append(get_meta_board(self.global_board))
        self.last_move = move

        # Check for win condition.
        winner = get_global_winner(self.global_board)
        if winner is not None:
            self.end_game(winner, agent)
            return False  # End game

        # Determine next local board
        self.directive = (move[0] % 3, move[1] % 3)
        next_local_board = get_local_board(self.global_board, self.directive)
        if is_player(get_winner_local_board(next_local_board)) or is_board_full(next_local_board, 0):
            self.directive = None

        return True  # Continue game.


    def start(self, agent1: UT3Agent, agent2: UT3Agent):
        self.__init__()  # Reset most things
        self.agent1: UT3Agent = agent1
        self.agent2: UT3Agent = agent2

        self.agent1.player_num = 1
        self.agent2.player_num = -1
        now = datetime.datetime.now()
        self.time = round(now.timestamp() * 1000)  # for log name
        self.game_data["start_timestamp"] = str(now)  # for log data
        self.game_data["players"] = (self.agent1.player_name, self.agent2.player_name)

    def play(self, agent1: UT3Agent, agent2: UT3Agent):
        self.start(agent1, agent2)

        # Game loop.
        while self.make_move(self.agent1) and self.make_move(self.agent2):
            pass

        return self.winner

    def end_game(self, winner, agent: UT3Agent):
        now = datetime.datetime.now()
        self.game_data["end_timestamp"] = str(now)  # for log data
        self.winner = winner
        if is_player(winner):
            if self.print_moves:
                print("{}({}) won".format(agent.player_name, 'X' if agent.player_num == 1 else 'O'))
        else:
            if self.print_moves:
                print("The game was tied")
        if self.log_games:
            self.game_data["moves"] = self.move_list
            if agent is not None:
                self.game_data["winner"] = agent.player_num
                self.game_data["winner_name"] = agent.player_name
            if self.error is not None:
                self.game_data["error"] = self.error
            if self.log_boards:
                # Numpy arrays need to be converted to lists to be serialized in json
                self.game_data["boards"] = [[[int(col) for col in row] for row in board] for board in self.global_boards]
                self.game_data["meta_boards"] = [[[int(col) if col is not None else None for col in row] for row in board] for board in self.meta_boards]

            log_prefix = self.log_prefix if self.log_prefix is not None \
                else self.agent1.player_name + "_" + self.agent2.player_name
            self.log_name = "logs\\{}_{}".format(log_prefix,
                                            self.time)
            with open(self.log_name, 'w') as outfile:
                json.dump(self.game_data, outfile, indent=4 if self.pretty_logs else None)

    def print_move(self, last_move, agent: UT3Agent):
        print("Move", self.move_number)
        print(agent.player_name)
        print("{} to {}".format(num_to_char[agent.player_num], last_move))
        print("Board:")
        print_global_board(self.global_board)
        print("Meta-board:")
        print_board(get_meta_board(self.global_board))
        print()
        print()


    def validate_move(self, global_board, next_local_board, move):
        # Check they actually provided a move
        if move is None:
            self.error = "Invalid move on turn {}. Move was None".format(self.move_number)
            return False

        move_index = (move[0] // 3, move[1] // 3)

        if next_local_board is not None:
            if move_index != next_local_board:
                self.error = "Invalid move on turn {}. Move {} was not in the local board {}" \
                    .format(self.move_number, move, next_local_board)
                return False

        if global_board[move] != 0:
            self.error = "Invalid move on turn {}. Move {} would overwrite an existing move" \
                .format(self.move_number, move)
            return False

        if get_winner_local_board(get_local_board(global_board, move_index)) != None:
            self.error = "Invalid move on turn {}. Move {} would write to a finished local board" \
                .format(self.move_number, move)
            return False

        return True

