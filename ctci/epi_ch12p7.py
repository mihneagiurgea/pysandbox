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

if __name__ == '__main__':
    import doctest
    doctest.testmod()
