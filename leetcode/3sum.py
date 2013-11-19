from bisect import bisect_left

def find_2sum(A, start, end, target):
    """Yield all unique tuples (i, j) such that A[i] + A[j] = target, and
    start <= i < j <= end. A must be sorted in increasing order."""
    i = start
    j = end
    while i < j:
        if A[i] + A[j] == target:
            yield (A[i], A[j])
            # In order to avoid duplicates, increase i to a new A[i] value.
            i += 1
            while i < j and A[i] == A[i-1]:
                i += 1
        elif A[i] + A[j] < target:
            i += 1
        else:
            j -= 1

def find_3sum(A):
    """
    >>> list(find_3sum([-1, 0, 1, 2, -1, -4, 2]))
    [(-1, 0, 1), (-1, -1, 2), (-4, 2, 2)]
    >>> list(find_3sum([-1, 0, 2, 2, 1, 2, -1, -4, 2, 2]))
    [(-1, 0, 1), (-1, -1, 2), (-4, 2, 2)]
    >>> list(find_3sum([-1, 0, 2, 2, 1, 2, -1, -4, 2, 2, 0]))
    [(-1, 0, 1), (-1, -1, 2), (-4, 2, 2)]
    >>> list(find_3sum([-1, 0, 2, 2, 1, 2, -1, -4, 2, 2, 0, 0]))
    [(0, 0, 0), (-1, 0, 1), (-1, -1, 2), (-4, 2, 2)]
    >>> list(find_3sum([-1, 0, 2, 2, 1, 2, -1, -4, 2, 2, 0, 0, 0]))
    [(0, 0, 0), (-1, 0, 1), (-1, -1, 2), (-4, 2, 2)]
    """
    A.sort()
    # Remove duplicates appearing > 3 times.
    j = 3
    for i in range(3, len(A)):
        if not A[i] == A[i-1] == A[i-2] == A[i-3]:
            A[j] = A[i]
            j += 1
    for k in range(2, len(A)):
        if A[k] == A[k-1]:
            if A[k] != A[k-2]:
                # In order to eliminate duplicates, only try to form sums
                # using A[k] and A[k-1], because sums using A[k] but not A[k-1]
                # will be duplicates.
                target = -2 * A[k]
                i = bisect_left(A, target, 0, k-1)
                if i < k-1 and A[i] == target:
                    yield (target, A[k], A[k])
            else:
                # Only consider (A[k-2], A[k-1], A[k]).
                if A[k] == 0:
                    yield (0, 0, 0)
        else:
            for a, b in find_2sum(A, 0, k-1, -A[k]):
                yield (a, b, A[k])

if __name__ == "__main__":
    import doctest
    doctest.testmod()


