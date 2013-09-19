def binary_search(l, u, f):
    """Binary search f(x) == 0 on ints in range [l, u]."""
    while l < u:
        m = l + (u - l) / 2
        v = f(m)
        if v == 0:
            return m
        elif v < 0:
            l = m + 1
        else:
            u = m - 1
    return l


def find_kth(A, B, k):
    """
    >>> find_kth([1, 3, 5, 7], [2, 4, 6, 8], 1)
    1
    >>> find_kth([1, 3, 5, 7], [2, 4, 6, 8], 2)
    2
    >>> find_kth([1, 3, 5, 7], [2, 4, 6, 8], 8)
    8
    >>> find_kth(range(1, 100, 2), range(2, 100, 2), 1)
    1
    >>> find_kth(range(1, 100, 2), range(2, 100, 2), 3)
    3
    >>> find_kth(range(1, 100, 2), range(2, 100, 2), 47)
    47
    >>> find_kth(range(1, 100, 2), range(2, 100, 2), 93)
    93
    """

    def cmp(i):
        """If we grab the first i elements from A and j = k - i from B,
        are these 2 slices compatible to finding our solution?

        Returns: -1 if i is too small, +1 if i is too big
        """
        j = k - i
        if i >= len(A) or j < 0:
            return +1
        if j >= len(B):
            return -1

        # General case.
        if i == 0 or (j > 0 and A[i-1] <= B[j-1]):
            if i == len(A) or B[j-1] <= A[i]:
                return 0
            else:
                return -1
        elif j == 0 or (i > 0 and B[j-1] < A[i-1]):
            if j == len(B) or A[i-1] <= B[j]:
                return 0
            else:
                return +1
        else:
            raise ValueError('Wtf?')

    i = binary_search(0, len(A), cmp)
    j = k - i
    if i == 0:
        return B[j-1]
    elif j == 0:
        return A[i-1]
    else:
        return max(A[i-1], B[j-1])

if __name__ == '__main__':
    # print find_kth([1, 3, 5, 7], [2, 4, 6, 8], 8)
    import doctest
    doctest.testmod()
