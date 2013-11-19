import unittest2 as unittest

from creature import Creature

class TestCreature(unittest.TestCase):

    def test_serialization(self):
        s = repr(Creature(4, 7))
        self.assertIn('4/7', s)
        self.assertNotIn('T', s)

        s = repr(Creature(4, 7, tapped=True))
        self.assertIn('4/7', s)
        self.assertIn('T', s)

    def test_from_string(self):
        creature = Creature(4, 7)
        for tapped in (False, True):
            creature.tapped = tapped
            other = Creature.from_string(repr(creature))
            self.assertEqual(creature.power, other.power)
            self.assertEqual(creature.toughness, other.toughness)
            self.assertEqual(creature.tapped, other.tapped)
