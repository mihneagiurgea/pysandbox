from collections import defaultdict

EPSILON = 1E-4


class CurrencyConverter(object):

    def __init__(self):
        self.graph = defaultdict(list)
        self.U = {}

    def add_conversion(self, rate1, currency1, rate2, currency2):
        self.add_arc(currency1, currency2, rate2 / rate1)
        self.add_arc(currency2, currency1, rate1 / rate2)

    def add_arc(self, x, y, w):
        self.graph[x].append((y, w))

    def query(self, amount, source, target):
        self.U = {source: 1.0}
        self.df(source)
        if target in self.U:
            return self.U[target] * amount
        else:
            return None

    def df(self, x):
        for y, w in self.graph[x]:
            if y not in self.U or (self.U[y] > self.U[x] * w + EPSILON):
                self.U[y] = self.U[x] * w
                self.df(y)


def solve(fname):
    f = open(fname)
    N = int(f.readline())

    currency_converter = CurrencyConverter()

    for i in xrange(N):
        strarr = f.readline().split()
        currency_converter.add_conversion(
            float(strarr[0]), strarr[1], float(strarr[3]), strarr[4])

    P = int(f.readline())
    for i in xrange(P):
        strarr = f.readline().split()
        result = currency_converter.query(float(strarr[0]), strarr[1], strarr[3])
        if result is None:
            print 0
        else:
            print '%.4f' % result

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        fname = __file__.replace('.py', '.txt')
    else:
        fname = sys.argv[1]
    solve(fname)
