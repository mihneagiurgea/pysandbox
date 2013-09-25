class API(object):

    def __init__(self, A):
        self._A = A
        self.N = len(A)

    def get_bit(self, i, j):
        return (self._A[i] & (1 << j)) != 0

def find_missing(api):

    N = api.N
    indexes = range(N)
    missing = 0
    bit_position = 0
    while indexes:
        expected_1s = (N + 1) / 2
        # print 'N = %d expected_1s(%d) = %d' % (N, bit_position, expected_1s)

        indexes_0 = []
        indexes_1 = []
        for index in indexes:
            bit = api.get_bit(index, bit_position)
            if bit:
                indexes_1.append(index)
            else:
                indexes_0.append(index)

        if len(indexes_1) != expected_1s:
            missing_bit = 1
            indexes = indexes_1
        else:
            missing_bit = 0
            indexes = indexes_0

        missing |= missing_bit << bit_position
        bit_position += 1
        if missing_bit == N & 1:
            N = N / 2
        else:
            N = (N - 1) / 2

        # print 'indexes: %s' % indexes
        # print 'missing: %s' % missing

    return missing

def test(N, missing=None):
    import random

    A = range(N + 1)
    if missing is None:
        missing = random.randint(0, N)
    A.remove(missing)

    api = API(A)
    # print 'A: %s (N = %d)' % (A, api.N)
    result = find_missing(API(A))
    if result != missing:
        print 'Expected: %d' % missing
        print 'Found   : %d' % result

def test_big(N):
    for i in xrange(N + 1):
        test(N, i)

if __name__ == '__main__':
    test_big(132)
    test_big(133)
    test_big(1 << 7)
    print 'Okay'