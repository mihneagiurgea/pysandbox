"""

"""
from collections import namedtuple

# Query(i, j, k, v):
# f(v(i), v(j), v(k)) = v, where
#   f(x, y, z) = min(x, y, z) + max(x, y, z)
#   v(i) integer, 0 <= i < N
Query = namedtuple("Query", ["i", "j", "k", "v"])

"""
min(x, y) = (x + y - |x - y|) / 2
min(x, y, z) = min( min(x, y), z) =
    = (min(x, y) + z - |min(x, y) - z|) / 2
    = ((x + y - |x - y|) / 2 + z - |(x + y - |x - y|) / 2 - z|) / 2
    = ((x + y - |x - y|) / 2 + 2z / 2 - |(x + y - |x - y|) / 2 - 2z / 2|) / 2
    = (x + y - |x - y| + 2z - |x + y - |x - y| - 2z|) / 4
max(x, y) = (x + y + |x - y|) / 2
max(x, y, z) = max( max(x, y), z) =
    = (max(x, y) + z + |max(x, y) - z|) / 2
    = (x + y + |x - y| + 2z + |x + y + |x - y| - 2z|) / 4
min(x, y, z) + max(x, y, z) =
    = (x + y - |x - y| + 2z - |x + y - |x - y| - 2z|) / 4 + (x + y + |x - y| + 2z + |x + y + |x - y| - 2z|) / 4
    = (x + y - |x - y| + 2z - |x + y - |x - y| - 2z| + x + y + |x - y| + 2z + |x + y + |x - y| - 2z|) / 4
    = (2x + 2y + 4z - |x + y - |x - y| - 2z| + |x + y + |x - y| - 2z|) / 4


|x| = x, if x >= 0, else -x
|x| = x * sgn(x)
sgn(x) = +1, if x >= 0, else -1

{
    |x| = 1
} <=>
{
    x * y = 1
    y = 1
}
"""

"""
Solve for N = 4:
assume v(0) = 0
Q(0, 1, 2) = x
    if v(0) <= v(1) <= v(2) => v(0) + v(2) == x
    if v(0) <= v(2) <= v(1) => v(0) + v(1) == x
    if v(1) <= v(0) <= v(2) => v(1) + v(2) == x
    if v(1) <= v(2) <= v(0) => v(0) + v(1) == x
    if v(2) <= v(0) <= v(1) => v(1) + v(2) == x
    if v(2) <= v(1) <= v(0) => v(0) + v(2) == x
Q(0, 1, 3) = y
    if y < x =>

Q(0, 1, 4)
"""


def f(x, y, z):
    return min(x, y, z) + max(x, y, z)


def matches(v, q):
    return f(v[q.i], v[q.j], v[q.k]) == q.v


def solve(queries):
    solutions = []
    V = max(q.v for q in queries) + 1
    v = [0] * 6
    for i in range(V):
        for j in range(V):
            for l in range(V):
                for k in range(V):
                    for m in range(V):
                        for n in range(V):
                            # Matches all queries?
                            v[0] = i
                            v[1] = j
                            v[2] = l
                            v[3] = k
                            v[4] = m
                            v[5] = n
                            if all([matches(v, q) for q in queries]):
                                solutions.append(v[:])

    print "Found %d matches:\n%s" % (len(solutions), "\n".join(map(str, solutions[:7])))


# 1 7 2 3 4 5
queries = [
    Query(0, 1, 2, 8),
    Query(1, 2, 3, 9),
    Query(2, 3, 4, 6),
    Query(3, 4, 5, 8),
    Query(4, 5, 0, 6),
    Query(5, 0, 1, 8),
    # Query(0, 1, 3, 8),
    # Query(0, 1, 4, 8),
    # Query(0, 1, 5, 8),
    # Query(0, 2, 3, 9),
    # Query(0, 2, 4, 4),
    # Query(1, 2, 3, 10),
]
solve(queries)
