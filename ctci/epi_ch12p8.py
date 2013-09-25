def compute_leftie(A):
    """Computes the "leftie" L of A such that:
        L[i] = min j such that A[j:i] >= A[i]
    >>> compute_leftie([1, 4, 5, 4, 6, 4, 3, 2])
    [0, 1, 2, 1, 4, 1, 1, 1]
    """
    stack = []
    L = range(len(A))
    for i in range(len(A)):
        j = i
        while stack and stack[-1][0] >= A[i]:
            j = stack.pop()[1]
        L[i] = j
        stack.append((A[i], j))
    return L

def max_skyline_area(H):
    """
    >>> max_skyline_area([1, 4, 5, 4, 6, 4, 3, 2, 2, 1])
    20
    >>> max_skyline_area([1, 4, 5, 4, 0, 4, 3, 2, 2, 1])
    12
    >>> max_skyline_area([1, 4, 1, 4, 0, 4, 3, 2, 2, 1])
    8
    """
    L = compute_leftie(H)
    # Reverse H to compute the "rightie" of H.
    H_rev = H[::-1]
    R_rev = compute_leftie(H_rev)
    R = [len(H) - r - 1 for r in R_rev[::-1]]

    best_area = -1
    for i in range(len(H)):
        # What's the best area with h = H[i]?
        current_area = H[i] * (R[i] - L[i] + 1)
        best_area = max(best_area, current_area)
    return best_area

if __name__ == '__main__':
    import doctest
    doctest.testmod()