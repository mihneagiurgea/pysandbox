import bisect

def solve(A, K):
    """Find the subarray of maximum length and sum <= K."""
    # Solution is in the form of (length, start, sum).
    solution = (None, None, None)

    V = []
    Vpos = []

    prefix_sum = 0
    for i in range(len(A)):
        prefix_sum += A[i]

        # Can we use A[0:i+1] as a solution?
        if prefix_sum <= K:
            current_solution = (i+1, 0, prefix_sum)
            solution = max(solution, current_solution)
        else:
            # Find minimum j such that we can use A[j+1:i+1] as a solution.
            # V[index] >= prefix_sum - K
            index = bisect.bisect_left(V, prefix_sum - K)
            if index < len(V):
                j = Vpos[index]
                current_solution = (i - j, j + 1, prefix_sum - V[index])
                solution = max(solution, current_solution)

        # Add current prefix to V.
        if not V or prefix_sum > V[-1]:
            V.append(prefix_sum)
            Vpos.append(i)

    return solution

if __name__ == '__main__':
    V = [(0, -1), (5, 0), (12, 1), (16, 5)]

    A = [5, 7, -3, 2, 1, 3, 0, 9]
    sol = solve(A, 6)
    print sol
    (max_len, start, _) = sol
    print A[start:start+max_len]
