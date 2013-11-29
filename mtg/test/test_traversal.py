import unittest

from game_state import GameState
from strategies import BruteForceStrategy
from traversal import DFSWalk


class TestTraversal(unittest.TestCase):

    GET_OUTCOME_TESTS = (
        ('20/20 (0/0): 10/10 vs 3/3', +1),
        ('20/20 (0/1): 10/10 vs 3/3', -1),
        ('20/20 (0/2): 10/10 vs 3/3', +1),
        ('20/20 (1/0): 10/10 vs 3/3', -1),
        ('20/20 (0/0): 7/7 vs 3/3, 3/3, 3/3', 0)
        # ('20/20 (0/0): 7/7 vs 3/3, 3/3, 3/3, 1/1', 0),
        # ('20/20 (0/0): 10/10 vs 3/3, 3/3, 3/3, 3/3, 1/1', -1),
    )

    def test_dfs_walk(self):
        strategy = BruteForceStrategy()
        for game_state_string, expected_outcome in self.GET_OUTCOME_TESTS:
            game_state = GameState.from_string(game_state_string)
            dfs_walk = DFSWalk(strategy)
            outcome = dfs_walk.walk(game_state)
            self.assertEqual(outcome, expected_outcome,
                             'incorrect outcome for %s' % game_state)
