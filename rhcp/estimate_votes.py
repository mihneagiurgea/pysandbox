import math

UPPER_BOUND = 100000

def fit_percent(percent):
    results = []
    # 1.21 -> 121
    p = int(percent * 100)
    for N in xrange(1000, UPPER_BOUND):
        x_float = N * percent / 100.0
        floor = int(math.floor(x_float))
        ceil = int(math.ceil(x_float))

        # Rounded down
        x = 10000 * floor / N
        # Rounded up
        y = (10000 * floor + N) / N
        if x == p or y == p:
            print 'N = %d x = %.2f p = %.2f' % (N, x_float, percent)
            results.append(N)
        # if N % 50000 == 0:
        #     print N
    return results

def fit_percentages(percentages):
    results = None
    for percent in percentages:
        partial = set(fit_percent(percent))
        if results is None:
            results = partial
        else:
            results = results.intersection(partial)
        print '%.2f -> %d partial results' % (percent, len(partial))
        print 'Results so far: %d' % len(results)
    return results

if __name__ == '__main__':
    percentages =   {u'Alternosfera': 1.21,
                     u'Byron': 2.7999999999999998,
                     u'Cargo': 3.6000000000000001,
                     u'Celelalte Cuvinte': 1.6100000000000001,
                     u'Coma': 2.7200000000000002,
                     u'E.M.I.L.': 4.2300000000000004,
                     u'Grimus': 12.77,
                     u'Les Elephants Bizzares': 1.8500000000000001,
                     u'OCS': 8.3200000000000003,
                     u'Sarmalele Reci': 1.1100000000000001,
                     u'Subcarpati': 7.2300000000000004,
                     u'Vama': 28.800000000000001,
                     u'Vita de Vie': 8.0099999999999998,
                     u'Zdob si Zdub': 14.74,
                     u'Zob': 1.01}
    # Total: 100.010000%
    results = fit_percentages(percentages.values())
    print len(fit_percent(1.01))