def preprocess(S):
    """
    >>> preprocess('aba')
    '^#a#b#a#$'
    """
    return '^#%s#$' % ('#'.join(S), )

def compute_P(S):
    """
    >>> compute_P('abaaba')
    [0, 1, 0, 3, 0, 1, 6, 1, 0, 3, 0, 1, 0]
    >>> compute_P('babcbabcbaccba')
    [0, 1, 0, 3, 0, 1, 0, 7, 0, 1, 0, 9, 0, 1, 0, 5, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0]
    """
    # Add a # character between adjacent characters from S.
    S = preprocess(S)

    N = len(S)
    P = [0] * N

    P[0] = 0
    C = 0
    R = 0
    for i in range(1, N-1):
        # Compute d = P[i]
        if i >= R:
            d = 0
        else:
            i_mirror = 2*C - i
            d = min(P[i_mirror], R-i)

        while S[i-d-1] == S[i+d+1]:
            d += 1
        P[i] = d
        if i + P[i] > R:
            C = i
            R = i + P[i]

    # print ' '.join(S[1:-1])
    # print ' '.join(map(str, P[1:-1]))

    return P[1:-1]

def count_palind(S):
    """
    >>> count_palind('abaaac')
    10
    """
    P = compute_P(S)
    return sum((i+1) / 2 for i in P)

# compute_P('babcbabcbaccba')
import doctest
doctest.testmod()