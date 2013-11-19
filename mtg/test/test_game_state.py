import unittest2 as unittest

from game_state import GameState
from test.helpers import *

class TestGameState(unittest.TestCase):

    FIXTURES = [
        '20/18 (0/0): 2/3 (T), 4/6 vs 0/7',
        '20/-2 (0/0):  vs 0/7'
    ]

    def setUp(self):
        self.game_state = random_game_state(9)

    def test_serialization(self):
        for s in self.FIXTURES:
            self.assertEqual(repr(GameState.from_string(s)), s,
                             'Invalid deserialize & serialize transformation')

    def test_combat_phase_one_blocker(self):
        game_state = GameState.from_string('20/20 (0/0): 2/3, 4/6 vs 3/1')
        cr1, cr2 = game_state.attacking_player_creatures # 2/3 and 4/6
        cr3 = game_state.defending_player_creatures[0] # 0/7

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

    # IMPLEMENT ME
    def test_combat_phase_one_blocker(self):
        game_state = GameState.from_string('20/20 (0/0): 2/3, 4/6 vs 3/1')
        cr1, cr2 = game_state.attacking_player_creatures # 2/3 and 4/6
        cr3 = game_state.defending_player_creatures[0] # 0/7

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