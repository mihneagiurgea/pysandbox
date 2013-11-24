import unittest

from creature_state import CreatureState
from factories import CreatureStateFactory

class TestCreatureState(unittest.TestCase):

    def test_equality(self):
        cr1 = CreatureStateFactory()
        cr2 = CreatureStateFactory(creature_type=cr1.creature_type)

        self.assertEqual(cr1, cr2)
        cr2.controlling_player += 1
        self.assertNotEqual(cr1, cr2)

    def test_serialization(self):
        for _ in range(5):
            cr = CreatureStateFactory(controlling_player=0)
            self.assertEqual(CreatureState.from_string(repr(cr), 0), cr)

    def test_tap_and_untap(self):
        creature_state = CreatureStateFactory(tapped=False)

        normalized = creature_state.normalize()
        creature_state.tap()
        self.assertNotEqual(creature_state.normalize(), normalized)

        normalized = creature_state.normalize()
        creature_state.untap()
        self.assertNotEqual(creature_state.normalize(), normalized)

    def test_attack(self):
        """Test that .attack() is saved when normalized."""
        state = CreatureStateFactory(tapped=False)

        normalized = state.normalize()
        state.attack()

        self.assertTrue(state.attacking)
        self.assertNotEqual(state.normalize(), normalized)

        state.remove_from_combat()
        self.assertEqual(state.normalize(), normalized)

    def test_block(self):
        """Test that .block(uid) is saved when normalized."""
        state = CreatureStateFactory(tapped=False)
        self.assertFalse(state.blocking)

        normalized = state.normalize()
        state.block(47)

        self.assertEqual(state.blocking, 47)
        self.assertNotEqual(state.normalize(), normalized)

        state.remove_from_combat()
        self.assertEqual(state.normalize(), normalized)

    def test_creature_type_attributes(self):
        """Test that the CreatureType attributes (power, toughness, etc.) can
        be accessed from a CreatureState instance."""
        creature_state = CreatureStateFactory()
        self.assertEqual(creature_state.power,
            creature_state.creature_type.power)
        self.assertEqual(creature_state.toughness,
            creature_state.creature_type.toughness)
