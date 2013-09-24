import bisect

def max_subarray_of_sum(A, K):
    """Find the maximum-length subarray of sum <= K.

    >>> A = [5, 7, -3, 2, 1, 3, 0, 9]
    >>> max_subarray_of_sum(A, 6)
    (5, 2, 3)
    >>> max_subarray_of_sum(A, 3)
    (5, 2, 3)
    >>> max_subarray_of_sum(A, 2)
    (3, 2, 0)
    >>> max_subarray_of_sum(A, 10)
    (6, 1, 10)
    """
    # Solution is in the form of (length, start, sum).
    solution = (None, None, None)

    # Insert a sentinel element at the beginning of A to simplify coding,
    # without modifying the input array.
    A = [0] + A
    V = [0]
    Vpos = [0]

    prefix_sum = 0
    for i in range(1, len(A)):
        prefix_sum += A[i]

        # Find minimum j such that we can use A[j+1:i+1] as a solution.
        # V[index] >= prefix_sum - K
        index = bisect.bisect_left(V, prefix_sum - K)
        if index < len(V):
            j = Vpos[index]
            current_solution = (i - j, j + 1, prefix_sum - V[index])
            solution = max(solution, current_solution)

        # Add current prefix to V.
        if prefix_sum > V[-1]:
            V.append(prefix_sum)
            Vpos.append(i)

    # Decrease the start index by 1 to convert to original array.
    return (solution[0], solution[1] - 1, solution[2])

def max_subarray_of_mean(A, K):
    """Find the maximum-length subarray of mean <= K.

    >>> A = [5, 7, -3, 2, 1, 3, 0, 9]
    >>> max_subarray_of_mean(A, 6)
    (8, 0, 3.0)
    >>> max_subarray_of_mean(A, 2)
    (6, 2, 2.0)
    >>> max_subarray_of_mean(A, 0)
    (3, 2, 0.0)
    >>> max_subarray_of_mean(A, 1)
    (5, 2, 0.6)
    """
    # Solution is in the form of (length, start, sum).
    solution = (None, None, None)

    # Build vector of prefix sums.
    S = []
    for a in A:
        prefix = float(a)
        if S:
            prefix += S[-1]
        S.append(prefix)

    # Let S'[i] = S[i] + K * i
    # Let V be all increasing (strict) elements from S', and Vpos their
    # corresponding positions.
    V = []
    Vpos = []

    for i in range(len(A)):
        current_solution = (i + 1, 0, S[i] / (i + 1))
        if current_solution[2] <= K:
            solution = max(solution, current_solution)

        # Find minimum j such that we can use A[j+1:i+1] as a solution.
        # V[index] >= prefix_sum - K
        index = bisect.bisect_left(V, S[i] - K * i)
        if index < len(V):
            j = Vpos[index]
            current_solution = (i - j, j + 1, (S[i] - S[j]) / (i - j))
            solution = max(solution, current_solution)

        # Compute S'[i], and add it to V, if needed.
        sp = S[i] + K * i
        if not V or sp > V[-1]:
            V.append(sp)
            Vpos.append(i)

    return solution

if __name__ == '__main__':
    import doctest
    doctest.testmod()
