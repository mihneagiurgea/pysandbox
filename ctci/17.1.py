from collections import defaultdict


def swap(a, b):
    print a, b
    a ^= b
    b ^= a
    a ^= b
    print a, b


def query(guess, solution):
    """
    >>> query('RGBY', 'GGRR')
    (1, 1)
    >>> query('RGBY', 'RGYB')
    (2, 2)
    >>> query('RGBY', 'GBYR')
    (0, 4)
    >>> query('RRRR', 'YGYG')
    (0, 0)
    """

    def count_colors(s):
        colors = defaultdict(int)
        for c in s:
            colors[c] += 1
        return colors

    hits = 0
    for i in xrange(4):
        if guess[i] == solution[i]:
            hits += 1

    guess_colors = count_colors(guess)
    solution_colors = count_colors(solution)

    pseudo_hits = 0
    for color in guess_colors:
        pseudo_hits += min(solution_colors[color], guess_colors[color])
    pseudo_hits -= hits

    return (hits, pseudo_hits)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
