
import numpy
from collections import deque

A = numpy.array([
    [2, -1],
    [1, 0] ])
B = numpy.array([
    [2, 1],
    [1, 0] ])
C = numpy.array([
    [1, 2],
    [0, 1] ])
I = numpy.array([
    [1, 0],
    [0, 1] ])

multipliers = (A, B, C)

def iter_pythagorean_triples():
    nr = 0
    base = (2, 1)
    while True:
        X = I
        x = nr
        while x:
            X = numpy.dot(X, multipliers[x % 3])
            x /= 3

        m, n = numpy.dot(X, base)
        triples = [
            m * m - n * n,
            2 * m * n,
            m * m + n * n ]
        triples.sort()
        yield triples

        nr += 1
        if nr % 10000 == 0:
            print 'Iterated through %d Pythagorean triples' % nr

def iter_pythagorean_triples_bf():
    """Iterate through all Pythagorean triples, in bf order (an infinity)"""
    queue = deque()
    queue.append((2, 1))
    while queue:
        node = queue.popleft()
        m, n = node
        triples = [
            m * m - n * n,
            2 * m * n,
            m * m + n * n ]
        triples.sort()
        yield triples

        queue.append(tuple( numpy.dot(A, node) ))
        queue.append(tuple( numpy.dot(B, node) ))
        queue.append(tuple( numpy.dot(C, node) ))

if __name__ == '__main__':
    count = 0
    for triples in iter_pythagorean_triples():
        print triples
        count += 1
        if count == 5:
            break