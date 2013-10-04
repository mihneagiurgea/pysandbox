def solve(A):
    """
    >>> len(solve([100, 5, 200, 1, 3]))
    1
    >>> solve([100, 4, 200, 1, 3, 2])
    [1, 2, 3, 4]
    >>> solve([5, 47, 3, 48, 7, 99, 9, 8, 4, 6])
    [3, 4, 5, 6, 7, 8, 9]
    """
    best = None
    # Maximum number of consecutive elements when starting from x,
    start = {}
    # and when ending in x.
    end = {}
    for a in A:
        start[a] = start.get(a+1, 0) + 1
        end[a] = end.get(a-1, 0) + 1

        i = a - end[a] + 1
        j = a + start[a] - 1
        start[i] = end[j] = j-i+1
        if best is None or start[best] < start[i]:
            best = i
    return range(best, best+start[best])


if __name__ == '__main__':
    import doctest
    doctest.testmod()