import random

def count_sort(A, key=None):
    """Stable-sort an array A of integers in range [0..K) in O(N + K) time.

    >>> A = [3, 3, 1, 4, 7, 1, 4, 4]
    >>> count_sort(A)
    >>> A
    [1, 1, 3, 3, 4, 4, 4, 7]
    >>> count_sort(A, key=lambda x: x / 2 if x % 2 else x)
    >>> A
    [1, 1, 3, 3, 7, 4, 4, 4]
    """
    # Use the identity function ( f(x) = x ) as default.
    if key is None:
        key = lambda x: x

    K = max([key(a) for a in A]) + 1
    count = [0] * K
    for a in A:
        count[key(a)] += 1
    total = 0
    for i in xrange(K):
        c = count[i]
        count[i] = total
        total += c

    # temp := A
    temp = [a for a in A]

    for a in temp:
        pos = count[key(a)]
        count[key(a)] += 1
        A[pos] = a

def radix_sort(A, base=16, key=None):
    """Stable sort A using radix-sort.

    >>> A = [4, 3, 24, 2, 1, 14, 12, 11, 13, 23]
    >>> radix_sort(A)
    >>> A
    [1, 2, 3, 4, 11, 12, 13, 14, 23, 24]
    >>> A = range(100)
    >>> random.shuffle(A)
    >>> radix_sort(A)
    >>> A == range(100)
    True
    >>> N = 9987
    >>> A = range(N)
    >>> random.shuffle(A)
    >>> radix_sort(A)
    >>> A == range(N)
    True
    >>> radix_sort(A, base=2)
    >>> A == range(N)
    True
    """
    # Use the identity function ( f(x) = x ) as default.
    if key is None:
        key = lambda x: x

    max_nr = max([key(a) for a in A])
    div = 1
    while div < max_nr:
        digit_key = lambda x: key(x) / div % base
        count_sort(A, digit_key)

        div *= base

if __name__ == '__main__':
    import doctest
    doctest.testmod()
