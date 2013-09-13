def coords(i, j, n):
    """
    (i, 0) -> (0, n-1-i)
    (0, i) -> (i, n-1)
    (i, n-1) -> (n-1, n-1-i)
    (n-1,i) -> (i, 0)
    More general:
    (i, k) -> (k, n-1-i)
    (k, i) -> (i, n-1-k)
    where k = 0 or n-1
    """
    return (j, n-1-i)

def rotate(A):
    n = len(A)
    for i in xrange(0, n/2):
        for j in xrange(0, n/2):
            x, y = i, j
            last = A[x][y]
            for _ in range(4):
                p, q = coords(x, y, n)
                t = A[p][q]
                A[p][q] = last
                last = t
                x, y = p, q

def make_matrix(n):
    A = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(i*n + j)
        A.append(row)
    return A

def print_matrix(A):
    for i in range(len(A)):
        for j in range(len(A)):
            print '%2d' % A[i][j],
        print
    print

if __name__ == '__main__':
    A = make_matrix(6)
    print_matrix(A)
    rotate(A)
    print_matrix(A)
    rotate(A)
    print_matrix(A)
    rotate(A)
    print_matrix(A)
    rotate(A)
    print_matrix(A)

    i, j = (2, 1)
    n = 6
    for _ in range(4):
        p, q = coords(i, j, n)
        print '(%d, %d) -> (%d, %d)' % (i, j, p, q)
        i, j = p, q
