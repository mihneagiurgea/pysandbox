from collections import defaultdict


def read(f):
    f.readline()
    D = []
    M = []
    for line in f:
        d, m = map(int, line.split())
        D.append(d)
        M.append(m)
    return (D, M)


def solve(D, M):
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
