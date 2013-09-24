from array import array
from collections import deque

# Ox and Oy offsets for each of the 4 neighbours.
OFFSETS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Free and blocked cells.
FREE_CELL = 'F'
BLOCKED_CELL = 'B'


def make_matrix(N, M):
    matrix = []
    for i in xrange(N):
        # row = array('c', [FREE_CELL] * M)
        row = [FREE_CELL] * M
        matrix.append(row)
    return matrix


def make_bordered_matrix(N, M):
    # Make a matrix bordered with blocked cells.
    matrix = make_matrix(N+2, M+2)
    for i in xrange(M+2):
        matrix[0][i] = BLOCKED_CELL
        matrix[N+1][i] = BLOCKED_CELL
    for i in xrange(N+2):
        matrix[i][0] = BLOCKED_CELL
        matrix[i][M+1] = BLOCKED_CELL
    return matrix


def read_area_matrix(f):
    N, M, B = map(int, f.readline().split())
    matrix = make_bordered_matrix(N, M)
    for i in xrange(B):
        x, y = map(int, f.readline().split())
        matrix[x+1][y+1] = BLOCKED_CELL
    return (matrix, N, M)


def lee(matrix, N, M, start_x, start_y):
    queue = deque()
    matrix[start_x][start_y] = BLOCKED_CELL
    queue.appendleft((start_x, start_y))
    while len(queue):
        x, y = queue.pop()
        for ox, oy in OFFSETS:
            if matrix[x + ox][y + oy] == FREE_CELL:
                matrix[x + ox][y + oy] = BLOCKED_CELL
                queue.appendleft((x + ox, y + oy))


def count_connected_components(matrix, N, M):
    """Returns number of connected components."""
    count = 0
    for i in xrange(1, N+1):
        for j in xrange(1, M+1):
            if matrix[i][j] == FREE_CELL:
                count += 1
                # "Cross off" this connected component by marking all visited
                # cells with "1" (blocked).
                lee(matrix, N, M, i, j)
    return count


def solve(f):
    P = int(f.readline())
    for i in xrange(P):
        matrix, N, M = read_area_matrix(f)
        print count_connected_components(matrix, N, M)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        fname = __file__.replace('.py', '.txt')
    else:
        fname = sys.argv[1]
    f = open(fname)
    solve(f)
