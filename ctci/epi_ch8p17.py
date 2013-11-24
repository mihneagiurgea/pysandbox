def solve(A):
    """
    >>> solve([6, 6, 6, 1])
    1
    >>> solve([1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6])
    6
    >>> solve([1, 2, 3, 4, 5, 1, 2, 3, 5, 1, 2, 3, 5])
    4
    >>> solve([1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 7, 6, 6, 6])
    7
    """
    mask = (1 << 32) - 1
    s0 = mask
    s1 = 0
    s2 = 0
    for x in A:
        nx = x ^ mask
        cs0 = (s2 & x) | (s0 & nx)
        cs1 = (s0 & x) | (s1 & nx)
        cs2 = (s1 & x) | (s2 & nx)
        s0, s1, s2 = cs0, cs1, cs2
    return s1

if __name__ == '__main__':
    import doctest
    doctest.testmod()