import unittest2 as unittest

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

    def test_serialization(self):
        for s in self.SERIALIZATION_FIXTURES:
            self.assertEqual(repr(GameState.from_string(s)), s,
                             'Invalid deserialize & serialize transformation')
        for _ in range(10):
            game_state = GameStateFactory.build_with_creatures()
            s = repr(game_state)
            self.assertEqual(repr(GameState.from_string(s)), s,
                             'Invalid deserialize & serialize transformation')

    def test_combat_phase_one_blocker(self):
        game_state = GameState.from_string('20/20 (0/0): 2/3, 4/6 vs 3/1')
        cr1, cr2, cr3 = game_state.battleground.creatures

        ca = game_state.make_combat_assignment()

        # Declare attackers
        ca.declare_attacker(cr1)
        ca.declare_attacker(cr2)
        game_state.declare_attackers(ca)
        # Declare blockers
        ca.declare_blocker(cr3, cr1)
        game_state.declare_blockers(ca)
        # Resolve combat damage (blockers ordering has been skipped).
        game_state.resolve_combat(ca)

        expected_state = '20/16 (1/0): 4/6 (T) vs '
        self.assertEqual(repr(game_state), expected_state)

    def test_combat_phase_one_attacker(self):
        game_state = GameState.from_string('20/20 (0/0): 4/6 vs 1/2, 2/2, 3/1')
        cr1, cr2, cr3, cr4 = game_state.battleground.creatures

        ca = game_state.make_combat_assignment()

        # Declare attackers
        ca.declare_attacker(cr1)
        game_state.declare_attackers(ca)
        # Declare blockers
        ca.declare_blocker(cr2, cr1)
        ca.declare_blocker(cr3, cr1)
        ca.declare_blocker(cr4, cr1)
        game_state.declare_blockers(ca)
        ca.order_blockers(cr1, [cr4, cr3, cr2])
        # Resolve combat damage (blockers ordering has been skipped).
        game_state.resolve_combat(ca)

        expected_state = '20/20 (1/0): vs 1/2'
        self.assertEqual(repr(game_state), expected_state)
