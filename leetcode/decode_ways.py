def num_decodings(s):
    """
    >>> num_decodings('12')
    2
    >>> num_decodings('26')
    2
    >>> num_decodings('1111')
    5
    """
    # D[i] = # of ways to decode string s[:i]
    D = [0] * (len(s) + 1)
    D[0] = 1
    for i in range(len(s)):
        D[i+1] = D[i]
        if i > 0 and int(s[i-1:i+1]) <= 26:
            D[i+1] += D[i-1]
    return D[len(s)]

if __name__ == '__main__':
    import doctest
    doctest.testmod()