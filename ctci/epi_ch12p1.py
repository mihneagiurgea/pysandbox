# Merge 2 skylines

def merge_rectangles(x1, y1, h1, x2, y2, h2):
    """Merge 2 rectangles into a skyline, and returns an array of up to
    3 disjoing rectanges, sorted by x.
    >>> merge_rectangles(0, 4, 1, 4, 8, 2)
    [(0, 4, 1), (4, 8, 2)]
    >>> merge_rectangles(2, 10, 2, 4, 8, 4)
    [(2, 4, 2), (4, 8, 4), (8, 10, 2)]
    >>> merge_rectangles(2, 7, 2, 4, 8, 4)
    [(2, 4, 2), (4, 8, 4)]
    """
    # Do the 2 rectangles intersect?
    if y1 <= x2 or y2 <= x1:
        result = [(x1, y1, h1), (x2, y2, h2)]
        # Default sort is by x.
        result.sort()
        return result

    # Assume x1 <= x2.
    if x1 > x2:
        # Swap the 2 rectangles.
        x1, y1, h1, x2, y2, h2 = x2, y2, h2, x1, y1, h1

    result = []
    result.append((x1, x2, h1))
    if y1 < y2:
        result.append((x2, y1, max(h1, h2)))
        result.append((y1, y2, h2))
    else:
        result.append((x2, y2, max(h1, h2)))
        result.append((y2, y1, h1))
    # Remove empty segments from result.
    result = [s for s in result if s[0] < s[1]]
    # Adjacent segments from result might have the same height - merge them.
    corrected_result = []
    corrected_result.append(result[0])
    for i in range(1, len(result)):
        t = corrected_result[-1]
        s = result[i]
        if s[2] == t[2]:
            corrected_result[-1] = (t[0], s[1], t[2])
        else:
            corrected_result.append(s)
    return corrected_result

def merge_skylines(A, B):
    result = []

    i = 0
    j = 0
    current_x = -1
    while i < len(A) and j < len(B):
        # Look at the first elements from A and B, truncated to current_x.
        x1, y1, h1 = A[i]
        x2, y2, h2 = B[j]
        x1 = max(x1, current_x)
        x2 = max(x2, current_x)

        # Is el1 or el2 empty?
        if x1 >= y1:
            i += 1
            continue
        if x2 >= y2:
            j += 1
            continue

        # Do el1 and el2 even intersect?
        if y1 <= x2 or y2 <= x1:
            if x1 < x2:
                result.append((x1, y1, h1))
                i += 1
            else:
                result.append((x2, y2, h2))
                j += 1
            continue

        # el1 and el2 intersect - consider the next "segment"
        if x1 == x2:
            segment = (x1, min(y1, y2), )

        # min(x1, x2) and max(x1, x2).
        # if x1 < x2:

        from_x = min(x1, x2)
        to_x = max(x1, x2)



        current_x = to_x






def determine_skyline(A, i, j):
    """Determine skyline for A[i:j].

    Returns: list of (xi, yi, hi) such that
    [xi, yi] does not intersect [xi+1, yi+1].
    """
    if j - i == 1:
        return [A[i]]
    m = (i + j) / 2
    left = determine_skyline(A, i, m+1)
    right = determine_skyline(A, m+1, j)
    return merge_skylines(left, right)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
