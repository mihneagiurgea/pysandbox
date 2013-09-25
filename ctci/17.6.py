def find_indexes(a):
    """Returns two indexes m, n such that by sorting A[m]...A[n], then
    the array A would be sorted AND n-m is minimum.

    >>> find_indexes([1, 5, 3, 7, 4, 9, 13])
    (1, 4)
    >>> find_indexes([5, 4, 3, 2, 1])
    (0, 4)
    >>> find_indexes([0, 1, 2, 3, 4, 5])
    (6, 6)
    >>> find_indexes([1, 5, 91, 9, 90, 97, 7, 11, 95, 99])
    (2, 8)
    >>> find_indexes([0, 1, 2, 3, 5, 4, 6, 7, 8, 9])
    (4, 5)
    """

    def find_index(a):
        # Find the maximum increasing subarray A[0]...A[i]
        i = 0
        while i + 1 < len(a) and a[i + 1] > a[i]:
            i += 1

        # Are all values in A[i+1]..A[N-1] >= A[i]? If not, decrease i
        # until either this is true, or until i < 0.
        for j in xrange(i+1, len(a)):
            while i >= 0 and a[i] > a[j]:
                i -= 1

        return i + 1

    m = find_index(a)
    b = [-x for x in reversed(a)]
    n = len(a) - find_index(b) - 1

    n = max(m, n)
    return (m, n)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
