import unittest

from combat_assignment import CombatAssignment


class TestCombatAssignment(unittest.TestCase):

    def test_instantiation(self):
        ca = CombatAssignment()
        ca[3].append(5)
        self.assertIsInstance(ca, CombatAssignment)

        ca = CombatAssignment({3: [4, 5], 10: ()})
        self.assertEqual(ca[3], (4, 5), 'lists should be converted to tuples')
        self.assertEqual(ca[10], ())

    def test_is_compatible(self):
        ca1 = CombatAssignment({1: (11, 12), 2: (21, ), 3: ()})
        with self.assertRaises(ValueError):
            ca1.is_reorder_of({})

        ca2 = CombatAssignment({1: (11, 12), 2: (21, )})
        self.assertFalse(ca1.is_reorder_of(ca2))
        self.assertFalse(ca2.is_reorder_of(ca1))

        ca2 = CombatAssignment({1: (12, 11), 2: (21, ), 3: ()})
        self.assertNotEqual(ca1, ca2)
        self.assertTrue(ca1.is_reorder_of(ca2))
        self.assertTrue(ca2.is_reorder_of(ca1))
