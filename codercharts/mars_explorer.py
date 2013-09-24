from collections import deque

# Free and blocked cells.
FREE_CELL = 'F'
BLOCKED_CELL = 'B'


def make_bordered_matrix(N, M):
    # Make a matrix bordered with blocked cells.
    matrix = [FREE_CELL] * (N * M)
    for i in range(M):
        matrix[0 * M + i] = BLOCKED_CELL
        matrix[(N-1) * M + i] = BLOCKED_CELL
    for i in range(N):
        matrix[i * M + 0] = BLOCKED_CELL
        matrix[i * M + M-1] = BLOCKED_CELL
    return matrix


def read_area_matrix(f):
    N, M, B = map(int, f.readline().split())
    N += 2
    M += 2
    matrix = make_bordered_matrix(N, M)
    for i in range(B):
        x, y = map(int, f.readline().split())
        pos = (x+1) * M + (y+1)
        matrix[pos] = BLOCKED_CELL
    return (matrix, N, M)


def lee(matrix, N, M, pos):
    # Offsets coordinates for a liniar array of size (N, M).
    OFFSETS = (-1, +1, -M, +M)

    queue = deque()
    matrix[pos] = BLOCKED_CELL
    queue.appendleft(pos)
    while len(queue):
        pos = queue.pop()

        for offset in OFFSETS:
            if matrix[pos + offset] == FREE_CELL:
                matrix[pos + offset] = BLOCKED_CELL
                queue.appendleft(pos + offset)


def count_connected_components(matrix, N, M):
    """Returns number of connected components."""
    count = 0
    for i in range(1, N):
        for j in range(1, M):
            pos = i * M + j
            if matrix[pos] == FREE_CELL:
                count += 1
                # "Cross off" this connected component by marking all visited
                # cells with "1" (blocked).
                lee(matrix, N, M, pos)
    return count


def solve(f):
    P = int(f.readline())
    for i in range(P):
        matrix, N, M = read_area_matrix(f)

        # for i in range(N):
        #     for j in range(M):
        #         print '%c ' % matrix[i*M+j],
        #     print

        print count_connected_components(matrix, N, M)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        fname = __file__.replace('.py', '.txt')
    else:
        fname = sys.argv[1]
    f = open(fname)
    solve(f)
