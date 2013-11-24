import copy
import unittest

from battleground_state import BattlegroundState
from creature_state import CreatureState
from test.helpers import *

class TestBattlegroundState(unittest.TestCase):

    SERIALIZATION_FIXTURES = [
        '2/3 (T), 4/6 vs 0/7',
        ' vs 0/7',
        ' vs '
    ]

    def test_creature_accessor(self):
        """Test that the creatures can be accessed via their uid."""
        bg = BattlegroundState()
        h1 = bg.normalize()
        uid = bg.add_creature(random_creature(), CreatureState(0))

        bg[uid].tap()
        self.assertNotEqual(bg.normalize(), h1)

    def test_normalize(self):
        bg = BattlegroundState()
        h1 = bg.normalize()

        uid = bg.add_creature(random_creature(), random_creature_state())
        h2 = bg.normalize()
        self.assertNotEqual(h1, h2)

        bg.remove_creature(uid)
        self.assertEqual(h1, bg.normalize())

    def test_equality(self):
        bg1 = BattlegroundState()
        uid1 = bg1.add_creature(random_creature(), random_creature_state())
        bg1.add_creature(random_creature(), random_creature_state())
        bg1.add_creature(random_creature(), random_creature_state())

        bg2 = copy.deepcopy(bg1)
        self.assertEqual(bg1, bg2)

        bg1.remove_creature(uid1)
        self.assertNotEqual(bg1, bg2)

    def test_equality_when_different_uids(self):
        """Test equality when creature uids differ."""
        bg1 = BattlegroundState()
        bg2 = BattlegroundState()

        uid1 = bg1.add_creature(random_creature(), random_creature_state())
        bg1.remove_creature(uid1)

        creature = random_creature()
        creature_state = random_creature_state()
        bg1.add_creature(creature, creature_state)
        bg2.add_creature(creature, creature_state)

        self.assertEqual(bg1, bg2)

    def test_equality_when_different_creature_order(self):
        """Test equality when creatures have been added in different orders."""
        bg1 = BattlegroundState()
        bg2 = BattlegroundState()

        creature1 = random_creature()
        creature_state1 = random_creature_state()
        creature2 = random_creature()
        creature_state2 = random_creature_state()

        bg1.add_creature(creature1, creature_state1)
        bg1.add_creature(creature2, creature_state2)

        bg2.add_creature(creature2, creature_state2)
        bg2.add_creature(creature1, creature_state1)

        self.assertEqual(bg1, bg2)

    def test_serialization(self):
        """Test repr and from_string methods together."""
        for s in self.SERIALIZATION_FIXTURES:
            self.assertEqual(repr(BattlegroundState.from_string(s)), s,
                             'Invalid deserialize & serialize transformation')
        for _ in range(10):
            state = random_battleground_state()
            s = repr(state)
            self.assertEqual(repr(BattlegroundState.from_string(s)), s,
                             'Invalid deserialize & serialize transformation')

    def test_get_combat_assignment(self):
        bg = BattlegroundState()

        creature_type = random_creature()
        creature_state1 = random_creature_state(0)
        creature_state1.attacking = True
        uid1 = bg.add_creature(creature_type, creature_state1)

        creature_state2 = random_creature_state(1)
        creature_state2.blocking = uid1
        creature_state3 = random_creature_state(1)
        creature_state3.blocking = uid1

        uid2 = bg.add_creature(creature_type, creature_state2)
        uid3 = bg.add_creature(creature_type, creature_state3)

        combat_assignment = bg.get_combat_assignment()
        expected = {
            uid1: [uid2, uid3]
        }
        self.assertEqual(combat_assignment, expected)
