def binary_search(A, B, k, left, right):
    while left < right:
        i = (left + right) / 2
        j = k - i - 1
        if A[i] < B[j] < A[i+1] or B[j] < A[i] < B[j+1]:
            return i, j

        if A[i] < B[j]:
            # Selected too few elements from A, increase i.
            left = i
        else:
            right = i
    return left, k - left - 1

def find_kth(A, B, k):
    """
    >>> find_kth([1, 3, 5, 7], [2, 4, 6, 8], 1)
    1
    >>> find_kth([1, 3, 5, 7], [2, 4, 6, 8], 2)
    2
    >>> find_kth([1, 3, 5, 7], [2, 4, 6, 8], 8)
    8
    >>> find_kth([4, 5, 6, 7, 8, 9], [1, 2, 3], 8)
    8
    >>> find_kth([4, 5, 6, 7, 8, 9], [1, 2, 3], 4)
    4
    >>> find_kth([4, 5, 6, 7, 8, 9], [1, 2, 3], 9)
    9
    >>> find_kth([4, 5, 6, 7, 8, 9], [1, 2, 3], 3)
    3
    >>> find_kth(range(1, 100, 2), range(2, 100, 2), 1)
    1
    >>> find_kth(range(1, 100, 2), range(2, 100, 2), 3)
    3
    >>> find_kth(range(1, 100, 2), range(2, 100, 2), 47)
    47
    >>> find_kth(range(1, 100, 2), range(2, 100, 2), 93)
    93
    >>> find_kth([100, 101, 102], range(1, 100), 93)
    93
    >>> find_kth(range(1, 100), [100, 101, 102], 93)
    93
    >>> find_kth([1, 2, 3], range(100, 200), 94)
    190
    >>> find_kth(range(100, 200), [1, 2, 3], 94)
    190
    """
    # After merging A and B and selecting the kth element, we will have used
    # i elements from A and j elements from B.

    # Decrease k to convert from 1-indexed to 0-indexed.
    k -= 1

    # Case 1: i == 0 (no elements from A are selected).
    if k < len(B) and B[k] < A[0]:
        return B[k]
    # Case 2: j == 0 (no elements from B are selected).
    if k < len(A) and A[k] < B[0]:
        return A[k]
    # Case 3: both i and j > 0, use binary search to find i.
    lower_bound = max(k - len(B), 0)
    upper_bound = min(k, len(A))

    # Append an infinite value to both arrays, then remove it.
    inf = max(A[-1], B[-1]) + 1
    A.append(inf)
    B.append(inf)

    i, j = binary_search(A, B, k, lower_bound, upper_bound)
    result = max(A[i], B[j])

    A.pop()
    B.pop()

    return result

def find_median_sorted_arrays(A, B):
    return find_kth(A, B, (len(A) + len(B)) / 2)

if __name__ == '__main__':
    import doctest
    doctest.testmod()