from collections import defaultdict


def read(f):
    N, K = map(int, f.readline().split())
    A = map(int, f.readline().split())
    return (A, K)


def solve(A, K):
    counts = defaultdict(int)

    result = 0
    for a in A:
        result += counts[a - K] + counts[a + K]
        counts[a] += 1
    return result

if __name__ == '__main__':
    import sys
    f = sys.stdin
    # f = open(__file__.replace(".py", ".txt"))
    print solve(*read(f))
