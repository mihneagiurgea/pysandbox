import unittest2 as unittest

import combinatorics


class TestCombinatorics(unittest.TestCase):

    def test_get_all_subsets(self):
        S = [1, 2, 3]
        subsets = list(combinatorics.get_all_subsets(S))
        self.assertEqual(len(subsets), 8)

        subsets = set(tuple(subset) for subset in subsets)
        self.assertEqual(len(subsets), 8)

    def test_get_all_mappings(self):
        R = ['a', 'b', 'c']
        T = ['A', 'B', 'C']
        mappings = list(combinatorics.get_all_mappings(R, T))
        self.assertEqual(len(mappings), 27)

        normalized = set()
        # Are all mappings unique and valid?
        for mapping in mappings:
            normalized.add(tuple(sorted(mapping.items())))
        self.assertEqual(len(normalized), 27)