def apply_perm(A, P):
    """
    >>> A = ['a', 'b', 'c', 'd', 'e']
    >>> apply_perm(A, [3, 1, 2, 5, 4])
    >>> A
    ['b', 'c', 'a', 'e', 'd']
    >>> apply_perm(A, [2, 3, 1, 5, 4])
    >>> A
    ['a', 'b', 'c', 'd', 'e']
    >>> A = ['a', 'b', 'c', 'd', 'e', 'f']
    >>> apply_perm(A, [2, 3, 1, 6, 5, 4])
    >>> A
    ['c', 'a', 'b', 'f', 'e', 'd']
    """
    N = len(P)
    for i in range(N):
        if P[i] >= 1:
            # Apply the cycle starting at position i.
            j = i

            last = A[j]
            while P[j] >= 1:
                next = P[j] - 1
                last, A[next] = A[next], last
                P[j] -= N
                j = next

    # Fix P
    for i in range(N):
        P[i] += N

def next_permutation_with_duplicates(A):
    """
    >>> next_permutation_with_duplicates([1, 3, 5, 4, 2])
    [1, 4, 2, 3, 5]
    >>> next_permutation_with_duplicates([1, 1, 1, 2, 2])
    [1, 1, 2, 1, 2]
    >>> next_permutation_with_duplicates([1, 1, 2, 1, 2])
    [1, 1, 2, 2, 1]
    """
    # Copy A into a new array.
    A = A[::]

    N = len(A)
    i = N - 2
    while i >= 0 and A[i] >= A[i+1]:
        i -= 1
    if i < 0:
        return None

    j = N - 1
    while A[j] <= A[i]:
        j -= 1
    # Now A[j] > A[i].
    A[i], A[j] = A[j], A[i]

    # Reverse A[i+1:].
    j = i+1
    while j < N - j + i:
        A[j], A[N-j+i] = A[N-j+i], A[j]
        j += 1

    return A

A = [1, 2, 2, 4, 5]
while A is not None:
    print A
    A = next_permutation_with_duplicates(A)

import doctest
doctest.testmod()