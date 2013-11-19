import unittest2 as unittest

from combat_assignment import CombatAssignment
from helpers import *

class TestCombatAssignment(unittest.TestCase):

    def setUp(self):
        self.game_state = random_game_state(11)
        self.ca = CombatAssignment(self.game_state)

    def test_declare_attacker(self):
        with self.assertRaises(ValueError):
            creature = self.game_state.defending_player_creatures[0]
            self.ca.declare_attacker(creature)
        with self.assertRaises(ValueError):
            creature = self.game_state.attacking_player_creatures[0]
            creature.tap()
            self.ca.declare_attacker(creature)
