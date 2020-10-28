import unittest
import replay_agent
import game

class TestUT3Game(unittest.TestCase):
    #TODO: Test next local board enforcement
    #TODO: Test recovery from invalid moves
    #TODO: Test detecting out of range moves
    #TODO: Test detecting agent not respecting next local board
    #TODO: Test moves should time out if they take too long
    #TODO: Test logging game moves
    #TODO: Test that tie games are culled early with replay file
    pass

    def test_tie_ends_early(self):
        """
        This is for a bug that where tie games weren't factored considered in is_board_winnable
        :return:
        """
        agent1, agent2 = replay_agent.get_replay_agents_from_file("tie_game_that_shouldnt_last_62_moves")
        test_game = game.UT3Game()
        test_game.log_games = False
        result = test_game.play(agent1, agent2)
        self.assertEqual(result, 0, "The game should be a draw")
        self.assertEqual(len(test_game.move_list), 60, "The game should tie after 60 moves")
