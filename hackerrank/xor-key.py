import math


def read(f):
    f.readline()
    A = map(int, f.readline().split())
    return (A,)

MAX_BIN_DIGITS = 15
MASK = 1 << MAX_BIN_DIGITS
ONES_MASK = MASK - 1
MAX_PREFIXES_VALUE = 1 << MAX_BIN_DIGITS

PREFIXES = []

def precompute_prefixes():
    for i in range(MAX_PREFIXES_VALUE):
        a = i ^ MASK
        prefixes = set()
        while a:
            prefixes.add(a)
            a >>= 1
        PREFIXES.append(prefixes)

precompute_prefixes()

XOR_DIGITS = []

def precompute_xor_digits():
    for i in range(MAX_PREFIXES_VALUE):
        a = i ^ ONES_MASK

        digits = [a >> shift & 1 for shift in range(MAX_BIN_DIGITS-1, -1, -1)]
        XOR_DIGITS.append(digits)

precompute_xor_digits()


class SegmentTree(object):
    """This is actually a SegmentTree of Tries, where each Trie is implemented
    as a simple set().
    """

    def __init__(self, size):
        self.size = 1 << int(math.ceil(math.log(size, 2)))
        self.tree = []
        for _ in xrange(2 * self.size):
            self.tree.append(set())

    def add(self, i, value):
        i = i + self.size - 1
        while value not in self.tree[i]:
            self.tree[i].add(value)
            i >>= 1

    def set_leaf(self, i, value):
        """Overrides the value of leaf responsible for position #i, without
        updating the leaf's parents. Must be used together with
        propagate_leaves."""
        self.tree[i + self.size - 1] = value

    def propagate_leaves(self):
        """Propagate all values from leafs upwards."""
        for i in range(self.size-1, 0, -1):
            left = self.tree[i << 1]
            right = self.tree[i << 1 | 1]
            self.tree[i] = left.union(right)

    # @profile
    def find_max_xor(self, a, prefixes):
        best_prefix = 1
        for digit in XOR_DIGITS[a]:
            best_prefix = (best_prefix << 1) | digit
            if best_prefix not in prefixes:
                best_prefix ^= 1
        return best_prefix

    # @profile
    def _query(self, node, node_left, node_right, left, right, a):
        # Is this node included in our search interval?
        if left <= node_left and node_right <= right:
            return a ^ self.find_max_xor(a, self.tree[node])

        result = -1
        middle = (node_left + node_right) >> 1
        if left <= middle:
            t = self._query(node << 1, node_left, middle, left, right, a)
            result = max(result, t)
        if middle + 1 <= right:
            t = self._query(node << 1 | 1, middle + 1, node_right, left, right, a)
            result = max(result, t)

        return result

    def query(self, left, right, a):
        """Performs the query on [left, right] interval."""
        # print 'Query(%d, %d, %d)' % (left, right, a)
        return self._query(1, 1, self.size, left, right, a)


if __name__ == '__main__':
    import sys
    f = sys.stdin
    f = open("input.txt")
    T = int(f.readline())
    for i in xrange(T):
        N, Q = map(int, f.readline().split())
        A = map(int, f.readline().split())

        segment_tree = SegmentTree(len(A))
        for i in range(0, len(A)):
            segment_tree.set_leaf(i + 1, PREFIXES[ A[i] ])
        segment_tree.propagate_leaves()

        # for idx, e in enumerate(segment_tree.tree):
        #     if e is None:
        #         e = set()
        #     print '%d: %r' % (idx, [bin(i) for i in sorted(e)])

        for _ in range(Q):
            a, p, q = map(int, f.readline().split())
            print segment_tree.query(p, q, a) ^ MASK
