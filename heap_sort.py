def heap_sort(A):
    """
    >>> A = [7, 5, 8, 6, 2, 3, 1, 4, 10, 9]
    >>> heap_sort(A)
    >>> A == sorted(A)
    True
    >>> A = range(19, 3, -1)
    >>> heap_sort(A)
    >>> A == sorted(A)
    True
    """
    def swap(i, j):
        A[i], A[j] = A[j], A[i]

    def sink(i, n):
        while True:
            # 0 -> (1, 2) | 1 -> (3, 4)
            l = 2 * i + 1
            if l >= n:
                break
            # position of max child
            mc = l
            r = l + 1
            if r < n and A[r] > A[l]:
                mc = r
            if A[mc] > A[i]:
                swap(i, mc)
                i = mc
            else:
                break

    n = len(A)
    for i in range(n/2, -1, -1):
        sink(i, n)

    for i in range(n-1):
        swap(0, n-i-1)
        sink(0, n-i-1)

if __name__ == '__main__':
    import doctest
    doctest.testmod()





