import unittest2 as unittest

from combat_assignment import CombatAssignment
from game_state import GameState
from factories import GameStateFactory

class TestGameState(unittest.TestCase):

    SERIALIZATION_FIXTURES = (
        '20/18 (0/0): 2/3 (T), 4/6 vs 0/7',
        '20/-2 (0/0):  vs 0/7',
        '-2/-2 (1/0):  vs '
    )

    def test_equality(self):
        game_state1 = GameStateFactory.build_with_creatures(9)
        game_state2 = GameStateFactory.build_with_creatures(8)

        self.assertNotEqual(game_state1, game_state2)

        game_state2.battleground = game_state1.battleground
        self.assertEqual(game_state1, game_state2)

        game_state1 = GameState.from_string('20/20 (1/0): vs 1/2')
        game_state2 = GameState.from_string('20/20 (1/0): vs 1/2')
        self.assertEqual(game_state1, game_state2)

    def test_serialization(self):
        for s in self.SERIALIZATION_FIXTURES:
            self.assertEqual(repr(GameState.from_string(s)), s,
                             'Invalid deserialize & serialize transformation')
        for _ in range(10):
            game_state = GameStateFactory.build_with_creatures()
            s = repr(game_state)
            self.assertEqual(repr(GameState.from_string(s)), s,
                             'Invalid deserialize & serialize transformation')

    def test_untap(self):
        game_state = GameState.from_string('20/20 (0/0): 2/3 (T), 4/6 (T) vs ')
        game_state.untap()

        expected_state = '20/20 (0/0): 2/3, 4/6 vs '
        self.assertEqual(repr(game_state), expected_state)

    def _prepare_game_state(self, string):
        game_state = GameState.from_string(string)
        uids = [t[0] for t in game_state.battleground.creatures_with_uids]
        uids.sort()
        uids.insert(0, game_state)
        return uids

    def test_resolve_combat_invalid_argument(self):
        """Test that resolve_combat raises an error when given an incorrect
        argument."""
        game_state, cr1, cr2, cr3 = \
            self._prepare_game_state('20/20 (0/0): 2/3, 4/6 vs 3/1')

        # Declare attackers 2/3 and 4/6
        game_state.declare_attackers([cr1, cr2])
        # Declare blockers 3/1 -> 2/3
        game_state.declare_blockers({cr3: cr1})

        combat_assignment = CombatAssignment({cr1: []})
        # Resolve combat damage, with arbitrary order of blockers.
        with self.assertRaises(ValueError):
            game_state.resolve_combat(combat_assignment)

    def test_combat_phase_one_blocker(self):
        game_state, cr1, cr2, cr3 = \
            self._prepare_game_state('20/20 (0/0): 2/3, 4/6 vs 3/1')

        # Declare attackers 2/3 and 4/6
        game_state.declare_attackers([cr1, cr2])
        # Declare blockers 3/1 -> 2/3
        game_state.declare_blockers({cr3: cr1})
        # Resolve combat damage, with arbitrary order of blockers.
        game_state.resolve_combat()

        expected = GameState.from_string('20/16 (1/0): 4/6 (T) vs ')
        print game_state.normalize()
        print expected.normalize()
        self.assertEqual(game_state, expected)

    def test_combat_phase_one_attacker(self):
        game_state, cr1, cr2, cr3, cr4 = \
            self._prepare_game_state('20/20 (0/0): 4/6 vs 1/2, 2/2, 3/1')

        # Declare attackers 4/6
        game_state.declare_attackers([cr1])
        # Declare blockers (everybody -> 4/6)
        game_state.declare_blockers({cr2: cr1, cr3: cr1, cr4: cr1})
        # Resolve combat damage after ordering blockers.
        combat_assignment = CombatAssignment({cr1: [cr4, cr3, cr2]})
        game_state.resolve_combat(combat_assignment)

        expected_state = '20/20 (1/0): vs 1/2'
        self.assertEqual(game_state, GameState.from_string(expected_state))
