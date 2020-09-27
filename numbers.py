import doctest


def partition(A, k):
    """
    In-place partitions A such that A[0:i] <= middle < A[i:], 
    where middle = A[k] at the time partition was called.

    Returns A.

    >>> partition([3, 1, 4, 5, 6, 8, 2], 4)
    [3, 1, 2, 4, 5, 6, 8]
    """
    middle = A[k]
    # Imagine two slices [smaller..->][<-], where potentially both may be
    # empty.
    # smaller array will be [:next_smaller]
    # larger array will be [next_larger:]
    next_smaller = 0  # smaller
    next_larger = len(A) - 1
    middle_pos = None
    for idx, elem in enumerate(A):
        if elem < middle:
            next_smaller += 1
        else:
            # swap A[idx], A[next_larger]
            A[idx], A[next_larger] = A[next_larger], A[idx]

            if elem == middle:
                middle_pos = idx


doctest.testmod()
