import unittest2 as unittest

from game_state import GameState
import strategies


class TestStrategies(unittest.TestCase):

    def test_get_all_subsets(self):
        S = [1, 2, 3]
        subsets = list(strategies.get_all_subsets(S))
        self.assertEqual(len(subsets), 8)

        subsets = set(tuple(subset) for subset in subsets)
        self.assertEqual(len(subsets), 8)

    def test_get_all_mappings(self):
        R = ['a', 'b', 'c']
        T = ['A', 'B', 'C']
        mappings = list(strategies.get_all_mappings(R, T))
        self.assertEqual(len(mappings), 27)

        normalized = set()
        # Are all mappings unique and valid?
        for mapping in mappings:
            normalized.add(tuple(sorted(mapping.items())))
        self.assertEqual(len(normalized), 27)


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
