def longest_substring(s):
    """
    >>> longest_substring('abcabcbb')
    'abc'
    >>> longest_substring('bbbbb')
    'b'
    >>> longest_substring('zabcadzzzdbabcazd')
    'bcadz'
    """
    best_i = 0
    best_j = 0

    # Current solution is s[i:j].
    i = j = 0
    chars = set()
    while j < len(s):
        if s[j] in chars:
            while s[i] != s[j]:
                chars.remove(s[i])
                i += 1
            i += 1
        else:
            chars.add(s[j])
        j += 1

        # Is the current solution better?
        if j - i > best_j - best_i:
            best_i, best_j = i, j
    return s[best_i:best_j]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
