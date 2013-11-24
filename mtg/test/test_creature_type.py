import unittest2 as unittest

from creature import CreatureType
from factories import CreatureTypeFactory

class TestCreatureType(unittest.TestCase):

    def test_equality(self):
        cr1 = CreatureTypeFactory()
        cr2 = CreatureTypeFactory(power=cr1.power+1)
        self.assertNotEqual(cr1, cr2)

        cr2 = CreatureType(power=cr1.power, toughness=cr1.toughness)
        self.assertEqual(cr1, cr2)

    def test_serialization(self):
        for _ in range(5):
            cr = CreatureTypeFactory()
            self.assertEqual(CreatureType.from_string(repr(cr)), cr)
