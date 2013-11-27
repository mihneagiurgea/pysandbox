import unittest2 as unittest

import combinatorics


class TestCombinatorics(unittest.TestCase):

    def test_get_all_subsets(self):
        S = [1, 2, 3]
        subsets = list(combinatorics.get_all_subsets(S))
        self.assertEqual(len(subsets), 8)

        hashable_subsets = [tuple(subset) for subset in subsets]
        self.assertNoDuplicates(hashable_subsets)

    def test_get_all_mappings(self):
        R = ['a', 'b', 'c']
        T = ['A', 'B', 'C']
        mappings = list(combinatorics.get_all_mappings(R, T))
        self.assertEqual(len(mappings), 27)

        hashable_mappings = []
        # Are all mappings unique and valid?
        for mapping in mappings:
            hashable_mappings.append(tuple(sorted(mapping.items())))
        self.assertNoDuplicates(hashable_mappings)

    def test_get_all_shuffled_mappings(self):
        mapping = {
            1: (4, ),
            2: (5, 6),
            3: (7, 8, 9),
            4: ()
        }
        shuffled_mappings = list(
            combinatorics.get_all_shuffled_mappings(mapping))
        self.assertEqual(len(shuffled_mappings), 12)

        hashable_mappings = []
        # Are all mappings unique and valid?
        for mapping in shuffled_mappings:
            items = sorted(mapping.items())
            # Convert each item to something hashable.
            items = [ (i[0], tuple(i[1])) for i in items ]
            hashable_mappings.append(tuple(items))
        self.assertNoDuplicates(hashable_mappings)

    def assertNoDuplicates(self, items):
        unique = list(set(items))
        self.assertEqual(len(unique), len(items),
                         'duplicate items found: %r' % items)
