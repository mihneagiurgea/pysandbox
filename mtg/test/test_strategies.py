import unittest2 as unittest

from game_state import GameState
import strategies


class TestBruteForceStrategy(unittest.TestCase):

    # A list of (game_state, expected_next_states) tuples.
    NEXT_STATES_FIXTURES = [
        (
            '20/20 (0/0): 2/3, 4/6, 1/1 (T) vs 3/1',
            (
                '20/20 (1/0): 2/3, 4/6, 1/1 (T) vs 3/1',
                '20/20 (0/1): 2/3 (TA), 4/6, 1/1 (T) vs 3/1',
                '20/20 (0/1): 2/3, 4/6 (TA), 1/1 (T) vs 3/1',
                '20/20 (0/1): 2/3 (TA), 4/6 (TA), 1/1 (T) vs 3/1'
            )
        ),
        (
            '20/20 (0/1): 2/3 (TA), 4/6 (TA), 1/1 (T) vs 3/1',
            (
                '20/20 (0/2): 2/3 (TA), 4/6 (TA), 1/1 (T) vs 3/1',
                '20/20 (0/2): 2/3 (TA), 4/6 (TA), 1/1 (T) vs 3/1 (B#1)',
                '20/20 (0/2): 2/3 (TA), 4/6 (TA), 1/1 (T) vs 3/1 (B#2)'
            )
        ),
        (
            '20/20 (0/2): 4/4 (TA), 3/5 (TA), 4/6 (TA) vs '
            '4/4 (B#1), 3/3 (B#2), 2/2 (B#2), 4/4 (B#3), 3/3 (B#3)',
            (
                '20/20 (1/0):  vs 3/3, 4/4',
                '20/20 (1/0):  vs 2/2, 4/4',
                '20/20 (1/0):  vs 3/3, 3/3',
                '20/20 (1/0):  vs 2/2, 3/3'
            )
        )
    ]

    def setUp(self):
        self.strategy = strategies.BruteForceStrategy()

    def test_get_next_states(self):
        for fixture in self.NEXT_STATES_FIXTURES:
            game_state = GameState.from_string(fixture[0])
            expected_next_states = fixture[1]
            iterator = self.strategy.get_next_states(game_state)
            next_states = map(repr, iterator)
            self.assertEqual(set(expected_next_states), set(next_states),
                             'incorrect get_next_states for %r' % game_state)
