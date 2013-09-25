# Neighbor offsets.
DX = (-1, 0, 1, 0)
DY = (0, 1, 0, -1)

def solve(A, S):
    # D[k] = {(x, y) : there is a solution for S[:k] that starts from A(x, y)}
    D = [set() for _ in range(len(S))]

    N = len(A)

    def inside(i, j):
        return 0 <= i < N and 0 <= j < N

    def neighbors(i, j):
        result = []
        for o in range(4):
            ni = i + DX[o]
            nj = j + DY[o]
            if inside(ni, nj):
                result.append((ni, nj))
        return result

    # Initialize D[0].
    for i in range(N):
        for j in range(N):
            if A[i][j] == S[0]:
                D[0].add((i, j))

    # Compute D[k-1] -> D[k]
    for k in range(1, len(S)):
        for i in range(N):
            for j in range(N):
                if A[i][j] == S[k]:
                    for coords in neighbors(i, j):
                        if coords in D[k-1]:
                            D[k].add((i, j))
                            break

    k = len(S) - 1
    if not D[k]:
        return None

    coords = D[k].pop()
    path = []
    while k >= 0:
        path.append(coords)
        for n_coords in neighbors(*coords):
            if n_coords in D[k-1]:
                coords = n_coords
                break
        k -= 1

    return path[::-1]

if __name__ == '__main__':
    A = [
        [1, 2, 3],
        [3, 4, 5],
        [5, 6, 7]
    ]
    S = [1, 3, 4, 6]
    print 'Path: %r' % solve(A, S)
