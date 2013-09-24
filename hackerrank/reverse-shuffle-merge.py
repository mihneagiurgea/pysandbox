from collections import defaultdict

def solve(S):
    """
    >>> solve('eggegg')
    'egg'
    >>> solve('abccba')
    'abc'
    >>> solve('ccbbaa')
    'abc'
    >>> solve('aabbcc')
    'cba'
    >>> solve('gaezgzageg')
    'agzeg'
    """
    # Reverse S
    S = S[::-1]

    # Count each character in S.
    count = defaultdict(int)
    for c in S:
        count[c] += 1

    need = {}
    for c in count:
        need[c] = count[c] / 2

    solution = []
    i = 0
    while len(solution) < len(S) / 2:
        min_char_at = -1
        while True:
            c = S[i]
            if need[c] > 0 and (min_char_at < 0 or c < S[min_char_at]):
                min_char_at = i
            count[c] -= 1
            if count[c] < need[c]:
                break
            i += 1

        # Restore all chars right of the minimum character.
        for j in range(min_char_at+1, i+1):
            count[S[j]] += 1

        need[S[min_char_at]] -= 1
        solution.append(S[min_char_at])

        i = min_char_at + 1
    return ''.join(solution)

if __name__ == '__main__':
    print solve(raw_input())
    import doctest
    doctest.testmod()



