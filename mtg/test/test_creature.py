import unittest2 as unittest

from creature import Creature
from test.helpers import *

class TestCreature(unittest.TestCase):

    def test_equality(self):
        cr1 = random_creature()
        cr2 = random_creature(cr1.power+1)
        self.assertNotEqual(cr1, cr2)

        cr1 = random_creature()
        cr2 = Creature(cr1.power, cr1.toughness)
        self.assertEqual(cr1, cr2)

    def test_serialization(self):
        for _ in range(5):
            cr = random_creature()
            self.assertEqual(Creature.from_string(repr(cr)), cr)
