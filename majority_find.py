from collections import defaultdict

def majority_find(A, k):
    """
    >>> majority_find([1, 2, 3, 1, 2, 3, 1], 3)
    1
    >>> majority_find([3, 3, 2, 2, 1, 1, 1], 3)
    1
    >>> majority_find([1, 1, 1, 2, 3, 4, 5], 3)
    1
    >>> majority_find([2, 3, 4, 5, 1, 1, 1], 3)
    1
    >>> majority_find(range(1, 10), 3) is None
    True
    """
    counts = {}
    for x in A:
        if x in counts:
            counts[x] += 1
        else:
            if len(counts) < k - 1:
                counts[x] = 1
            else:
                for y in counts.keys():
                    counts[y] -= 1
                    if counts[y] == 0:
                        del counts[y]

    freq = defaultdict(int)
    for x in A:
        if x in counts:
            freq[x] += 1
    for x in freq:
        if freq[x] > len(A) / k:
            return x
    return None

if __name__ == '__main__':
    import doctest
    doctest.testmod()