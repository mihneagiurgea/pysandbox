def read(f):
    f.readline()
    A = map(int, f.readline().split())
    return (A, )


def compute_max_k(bit_nr, A, n, ignore_last=True):
    """
    Args:
        bit_nr: the bit number (1 means rightmost bit) to consider
        A: the total available pool of numbers
        n: the number of numbers to maximize for
    """
    if (bit_nr == 0):
        # No solution exists.
        return -1

    # Invariant: || A || >= n
    assert len(A) >= n

    def get_bit(x):
        return 1 if x & (1 << (bit_nr - 1)) else 0

    # Reduce each number from A to a single bit, then count number of zeros
    # and ones.
    nr_zeros = nr_ones = 0
    for a in A:
        if get_bit(a):
            nr_ones += 1
        else:
            nr_zeros += 1

    # How many "ones" can we get in M(B), Bi ^ Bi+1 = 1 - how many positions
    # can we solve at the current bit number?
    solved = 2 * min(nr_zeros, nr_ones)

    # How many positions do we need to solve?
    needed = n - 1 if ignore_last else n

    if solved >= needed:
        return bit_nr
    else:
        majoritary_bit = 1 if nr_ones > nr_zeros else 0
        Ap = [a for a in A if get_bit(a) == majoritary_bit]
        if not ignore_last:
            return compute_max_k(bit_nr - 1, Ap, n - solved + 1)
        else:
            return compute_max_k(bit_nr - 1, Ap, n - solved)


def solve(A):
    m = max(A)
    max_nr_bits = len(bin(m)) - 2
    return compute_max_k(max_nr_bits, A, len(A), ignore_last=False) - 1

if __name__ == '__main__':
    import sys
    f = sys.stdin
    f = open(__file__.replace(".py", ".txt"))
    print solve(*read(f))
