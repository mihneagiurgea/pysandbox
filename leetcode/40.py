def solve(A):
    """
    >>> solve([1, 7, 3, 5, 4, 2, 100])
    6
    >>> solve([-2, 5, 3, -4, 0])
    1
    >>> solve([-2, 5, 3, 1, 0])
    2
    >>> solve([2, 5, 3, 1, 0])
    4
    """
    N = len(A)
    for i in range(N):
        j = i
        el = A[i]
        # While element is not in its place, keep moving it...
        while 1 <= el <= N and el != j+1:
            j = el - 1
            el, A[j] = A[j], el
    for i in range(N):
        if A[i] != i+1:
            return i+1
    return N+1

import doctest
doctest.testmod()