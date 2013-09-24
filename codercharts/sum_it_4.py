import sys
from math import sqrt


def read(fname):
    nrs = map(int, open(fname).readlines())
    N = int(sqrt(len(nrs)))

    matrix = []
    for i in xrange(N):
        matrix.append([])

    curr_row = 0
    for nr in nrs:
        matrix[curr_row].append(nr)
        if len(matrix[curr_row]) == N:
            curr_row += 1

    return matrix


def max_subarray(A):
    max_sum = 0
    curr_sum = 0
    for a in A:
        curr_sum += a
        max_sum = max(max_sum, curr_sum)
        curr_sum = max(curr_sum, 0)
    return max_sum


def solve(matrix):
    max_sum = 0
    N = len(matrix)
    for i in xrange(N):
        sums = [0] * N
        for j in xrange(i, N):
            # sums += matrix[j]
            for l in xrange(N):
                sums[l] += matrix[j][l]
            max_sum = max(max_sum, max_subarray(sums))
    return max_sum

if __name__ == '__main__':
    if len(sys.argv) == 1:
        fname = __file__.replace('.py', '.txt')
    else:
        fname = sys.argv[1]
    print solve(read(fname))
