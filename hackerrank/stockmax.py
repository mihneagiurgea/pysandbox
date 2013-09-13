def read(f):
    f.readline()
    A = map(int, f.readline().split())
    return (A,)


def solve(A):
    result = 0
    max_stock = 0
    for a in reversed(A):
        result += max(max_stock - a, 0)
        max_stock = max(max_stock, a)
    return result

if __name__ == '__main__':
    import sys
    f = sys.stdin
    f = open(__file__.replace(".py", ".txt"))
    T = int(f.readline())
    for i in xrange(T):
        print solve(*read(f))
