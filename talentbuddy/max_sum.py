def range_sum(i, j):
    # Return sum of range(i, j).
    return j * (j - 1) / 2 - i * (i - 1) / 2

def max_sum_from_range(i, j):
    # Find max sum from range(i, j) = [i, i+1, ... j-1]
    if (j - i) % 2 == 0:
        # Use i+1, i+3, ... j-1.
        return ( range_sum(i, j) + (j - i) / 2 ) / 2
    else:
        # Use i, i+2, ... j-1.
        return max_sum_from_range(i+1, j) + i

def find_max_sum(v):
    """Given a list of integer numbers, find the maximum-sum subsequence that
    doesn't contain consecutive integers (if integer i is in subsequence,
    then i-1 and i+1 are not).
    >>> find_max_sum([1, 2, 3, 4])
    6
    >>> find_max_sum([1, 2, 3, 4, 5])
    9
    >>> find_max_sum([2, 5, 6, 5, 3])
    9
    >>> find_max_sum([3, 12, 4, 12, -3, 2, 0, 1, 10, -1, 11])
    28
    """
    # Step 1 - convert v into a hash (set), ignoring non-positive integers,
    # since they can't help with the solution.
    s = set(i for i in v if i > 0)

    result = 0
    # Step 2 - find all numbers i such that (i-1) not in s.
    for i in s:
        if i - 1 not in s:
            # Step 3 - determine max j such that range(i, j) in s.
            j = i
            while j in s:
                j += 1
            result += max_sum_from_range(i, j)

    print result

if __name__ == '__main__':
    import doctest
    doctest.testmod()





