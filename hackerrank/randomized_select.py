def partition(A, p, r):
    pivot = A[r]
    i = p - 1
    for j in xrange(p, r):
        # Invariant:
        # A[p..i] <= pivot < A[i+1..j]
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    # Swap A[r] (pivot) with A[i+1] to obtain:
    # A[p..i] <= A[i+1] < A[i+2..j]
    A[i+1], A[r] = A[r], A[i+1]
    return i + 1


def select(A, K, i=0, j=None):
    """Select the Kth smallest number (indexed from 1) from A[i]...A[j]."""
    if j is None:
        j = len(A) - 1
    if (i == j):
        return A[i]

    p = partition(A, i, j)
    # A[i..p-1] <= A[p] < A[p+1..j]
    if p - i + 1 == K:
        return A[p]
    elif p - i + 1 > K:
        return select(A, K, i, p-1)
    else:
        return select(A, K - (p - i + 1), p+1, j)
