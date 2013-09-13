class BinaryIndexedTree(object):

    @classmethod
    def lastbit(cls, x):
        """Finds the last non-zero bit in x."""
        return x & (-x)

    def __init__(self, max_value):
        self.max_value = max_value
        self.tree = [0] * (max_value + 1)

    def __getitem__(self, key):
        """Returns A[key]."""
        return self.query(key) - self.query(key-1)

    def __setitem__(self, key, value):
        """Performs A[key] = value, by adding or incrementing its value."""
        current = self[key]
        self.add(key, value - current)

    def add(self, i, value):
        """Performs A[i] += value"""
        if value == 0:
            return
        while i <= self.max_value:
            self.tree[i] += value
            i += self.lastbit(i)

    def query(self, i):
        """Returns prefix sum of A[1] + A[2] + ... + A[i]."""
        result = 0
        while i:
            result += self.tree[i]
            i -= self.lastbit(i)
        return result


def read(f):
    f.readline()
    return (map(int, f.readline().split()), )


def normalize(A):
    B = sorted(set(A))
    normalized = {}
    for i, b in enumerate(B):
        normalized[b] = i + 1
    return [normalized[a] for a in A]


def solve(A):
    A = normalize(A)
    max_value = max(A)

    # Frequency of each element.
    freqs = BinaryIndexedTree(max_value)
    # tuples[i] = # ascending tuples we can creating using i as the 2nd number
    tuples = BinaryIndexedTree(max_value)
    # triples[i] = # ascentind triples we can create using i as the 3rd number
    triples = BinaryIndexedTree(max_value)

    for a in A:
        triples[a] = tuples.query(a-1)
        # print "%d -> %d" % (a, triples[a])

        # How many ascending tuples can we form using "a" as the 2nd number?
        t = freqs.query(a-1)
        # In order to avoid duplicates, set value to "t", instead of
        # incrementing by "t".
        tuples[a] = t
        # ...and consider element "a" appears only once (counting it twice
        # would create duplicates later on).
        freqs[a] = 1

    print triples.query(max_value)

if __name__ == '__main__':
    import sys
    f = sys.stdin
    f = open(__file__.replace(".py", ".txt"))
    solve(*read(f))
