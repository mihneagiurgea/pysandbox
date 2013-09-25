def max_2d_square_subarray(A):
    N = len(A)
    M = len(A[0])

    # D[i][j] = L max : exists a square with bottomr right corner in (i, j)
    D = [[0] * M for _ in range(N)]
    for i in range(M):
        if A[0][i]:
            D[0][i] = 1
    for i in range(N):
        if A[i][0]:
            D[i][0] = 1

    # (len, i, j)
    solution = (None, None, None)

    for i in range(1, N):
        for j in range(1, M):
            if A[i][j] == 1:
                if D[i-1][j] == D[i][j-1]:
                    L = D[i-1][j]
                    if A[i-L][j-L]:
                        D[i][j] = L + 1
                    else:
                        D[i][j] = L
                else:
                    D[i][j] = min(D[i-1][j], D[i][j-1]) + 1
            current_solution = (D[i][j], i, j)
            solution = max(solution, current_solution)

    return solution


if __name__ == '__main__':
    A = [
        [0, 0, 0, 1, 1, 1],
        [0, 1, 0, 1, 1, 1],
        [1, 1, 0, 1, 1, 1]
    ]
    print max_2d_square_subarray(A)
