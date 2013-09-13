from collections import defaultdict


def read(f):
    A, B = map(int, f.readline().split())
    return (A, B)


def is_prime(k):
    if k < 2:
        return False
    if k <= 3:
        return True
    if k % 2 == 0:
        return False
    i = 3
    while i * i <= k:
        if k % i == 0:
            return False
        i += 2
    return True


def precompute_D(max_digits=18):
    """Compute the hashtable D with the following meaning:

    D[digits][ds][sds] = # of ways to obtain digit sum 'ds' and squared digit
        sum 'sds' using 'digits' digits, inclusing trailing 0s
    """
    D = {}

    # Initialize D[0].
    D[0] = {0: {0: 1}}

    # Precompute list of all digits and their squares to save time.
    DIGITS_AND_SQUARES = [(i, i ** 2) for i in xrange(10)]

    for nr_digits in xrange(1, max_digits + 1):
        D_curr = defaultdict(lambda: defaultdict(int))
        for ds, tempdict in D[nr_digits - 1].iteritems():
            for sds, count in tempdict.iteritems():
                for digit, squared_digit in DIGITS_AND_SQUARES:
                    D_curr[ds + digit][sds + squared_digit] += count
        D[nr_digits] = D_curr
        print '%d digits: %d len' % (nr_digits, len(D_curr))

    return D


class Solver(object):

    def __init__(self):
        self.D = precompute_D()
        # self.primes = set(p for p in range(2000) if is_prime(p))
        self.primes = [is_prime(p) for p in range(2000)]
        self.cache = {}

    def query(self, A, B):
        return self._query(B) - self._query(A-1)

    def _count_matches(self, digits, prefix_sum, prefix_squared_sum):
        key = (digits, prefix_sum, prefix_squared_sum)
        if key in self.cache:
            return self.cache[key]

        result = 0
        for ds, tempdict in self.D[digits].iteritems():
            if self.primes[ds + prefix_sum]:
                for sds, count in tempdict.iteritems():
                    if self.primes[sds + prefix_squared_sum]:
                        result += count

        self.cache[key] = result
        return result

    def _query(self, x):
        result = 0
        digits = [int(d) for d in str(x)]

        prefix_sum = 0
        prefix_squared_sum = 0
        for idx, digit in enumerate(digits):
            remaining_digits = len(digits) - idx - 1
            # print 'remaining_digits: %d' % remaining_digits
            for i in xrange(0, digit):
                result += self._count_matches(
                    remaining_digits,
                    prefix_sum + i,
                    prefix_squared_sum + i * i)

            prefix_sum += digit
            prefix_squared_sum += digit * digit

        if self.primes[prefix_sum] and self.primes[prefix_squared_sum]:
            result += 1

        # print 'Q(%d) = %d' % (x, result)
        return result


if __name__ == '__main__':
    import sys
    f = sys.stdin
    f = open(__file__.replace(".py", ".txt"))

    solver = Solver()

    T = int(f.readline())
    for i in xrange(T):
        A, B = read(f)
        print solver.query(A, B)
