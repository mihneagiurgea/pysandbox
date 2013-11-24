def search_in_rotated_sorted_array(A, value):
    """
    >>> search_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 6)
    2
    >>> search_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 0)
    4
    >>> search_in_rotated_sorted_array([5, 6, 7, 0, 1, 2, 4], 6)
    1
    """

    def find_pivot(A):
        left = 0
        right = len(A) - 1
        while left < right:
            if A[left] < A[right]:
                return left
            middle = left + (right - left) / 2
            if A[left] < A[middle]:
                left = middle + 1
            else:
                right = middle
        return left

    def binary_search(A, left, right, value):
        while left < right:
            middle = left + (right - left) / 2
            if value == A[middle]:
                return middle
            elif value < A[middle]:
                right = middle - 1
            else:
                left = middle + 1
        if A[left] == value:
            return left
        else:
            return -1

    pivot = find_pivot(A)
    index = binary_search(A, 0, pivot-1, value)
    if index >= 0:
        return index
    else:
        return binary_search(A, pivot, len(A)-1, value)

import doctest
doctest.testmod()