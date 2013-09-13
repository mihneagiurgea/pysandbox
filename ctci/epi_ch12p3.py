import math
import sys

def partition(A, p, r, pivot=None):
    """
    >>> partitioned = lambda A, k: max(A[:k]) <= A[k] and A[k] < min(A[k+1:])
    >>> A = [7, 1, 6, 2, 5, 3, 4]
    >>> partition(A, 0, len(A) - 1)
    3
    >>> partitioned(A, 3)
    True
    >>> A = [2, 8, 7, 1, 3, 5, 6, 4]
    >>> partition(A, 0, len(A) - 1)
    3
    >>> partitioned(A, 3)
    True
    """
    if pivot is None:
        pivot = A[r]
    i = p - 1
    for j in range(p, r+1):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    return i

def select(A, rank, p=0, r=None):
    """Select element with `rank` (1-indexed) from A[p:r+1].
    >>> import random
    >>> A = range(1, 23)
    >>> random.shuffle(A)
    >>> select(A, 4)
    4
    >>> random.shuffle(A)
    >>> select(A, 17)
    17
    """
    if r is None:
        r = len(A) - 1
    if p == r:
        return A[p]
    k = partition(A, p, r)
    if rank == k - p + 1:
        return A[k]
    elif rank < k - p + 1:
        return select(A, rank, p, k-1)
    else:
        return select(A, rank - (k - p + 1), k+1, r)

def dist(p1, p2):
    return math.sqrt( (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 )

def closest_distance(points, p, r):
    """Return the closest distance between 2 points in A[p:r+1]."""
    count = r - p + 1
    if count == 1:
        return sys.maxint
    if count == 2:
        return dist(points[p], points[r])
    median_pt = select(points, count / 2, p, r)
    k = partition(points, p, r, pivot=median_pt)
    x = median_pt[0]

    d1 = closest_distance(points, p, k)
    d2 = closest_distance(points, k+1, r)
    d = min(d1, d2)

    strip_points = []
    for pt in points[p:r+1]:
        if abs(pt[0] - x) <= d:
            strip_points.append(pt)

    strip_points.sort(key=lambda pt: pt[1])
    j = 0
    for i in range(1, len(strip_points)):
        while j < i and strip_points[i][1] - strip_points[j][1] > d:
            j += 1
        for l in range(j, i):
            d = min(d, dist(strip_points[l], strip_points[i]))
    return d

def test():
    points = [
        (5, 5),
        (4, 1),
        (6, 2),
        (3, 8),
        (9, 4),
        (1, 1),
        (11, 7),
        (2, 4),
        (12, 6)
    ]
    print closest_distance(points, 0, len(points)-1)

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    test()