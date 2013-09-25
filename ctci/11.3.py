def search(a, x, left=0, right=None):
    """Search element x in array a[left:right].

    Array a is sorted in increasing order, then rotated by an unknown offset.
    >>> a = [7, 8, 9, 1, 2, 3, 4, 5, 6]
    >>> search(a, 1)
    3
    >>> search(a, 8)
    1
    >>> search(a, 5)
    7
    >>> search(a, 10)
    -1
    >>> search(a, 2.5)
    -1
    >>> a = [4, 5, 6, 7, 8, 9, 1, 2, 3]
    >>> search([4, 5, 6, 7, 8, 9, 1, 2, 3], 1)
    6
    >>> search(a, 8)
    4
    >>> search(a, 5)
    1
    >>> search(a, 10)
    -1
    >>> search(a, 2.5)
    -1
    """
    if right is None:
        right = len(a)

    # print 'a[%d:%d]: %r' % (left, right, a[left:right])

    # Stop when we have <= 2 elements left
    if right - left <= 2:
        if a[left] == x:
            return left
        elif a[right-1] == x:
            return right-1
        else:
            return -1

    mid = (left + right) / 2
    if a[left] < a[mid]:
        # First half is correctly sorted.
        if a[left] <= x <= a[mid]:
            return search(a, x, left, mid+1)
        else:
            return search(a, x, mid+1, right)
    else:
        # Second half is correctly sorted.
        if a[mid] < x <= a[right-1]:
            return search(a, x, mid+1, right)
        else:
            return search(a, x, left, mid+1)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
