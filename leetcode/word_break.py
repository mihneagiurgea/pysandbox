def kmp_prefix_function(T):
    """
    >>> kmp_prefix_function('ababaa')
    [0, 0, 1, 2, 3, 1]
    """
    pi = [0] * len(T)
    j = 0
    for i in range(1, len(T)):
        while j and T[j] != T[i]:
            j = pi[j-1]
        if T[j] == T[i]:
            j += 1
        pi[i] = j
    return pi

def kmp_find_substrings(T, S):
    """Find all substrings in text S of pattern T.

    >>> kmp_find_substrings('aba', 'bbababaab')
    [2, 4]
    >>> kmp_find_substrings('aba', 'xxxabbaabababaxbab')
    [7, 9, 11]
    >>> kmp_find_substrings('ababaa', 'ababaaxabbabaa')
    [0]
    """
    pi = kmp_prefix_function(T)

    indices = []
    # How many characters have we successfully matched from T for position i?
    j = 0
    for i in range(len(S)):
        while j and T[j] != S[i]:
            j = pi[j-1]
        if T[j] == S[i]:
            j += 1
        if j == len(T):
            indices.append(i - len(T) + 1)
            j = pi[j-1]
    return indices

from collections import defaultdict

def word_break(S, words):
    """
    >>> word_break('leetcoder', ['leet', 'coder'])
    True
    >>> word_break('leetcode', ['leet', 'coder'])
    False
    """
    end_to_start = defaultdict(list)
    for word in words:
        indices = kmp_find_substrings(word, S)
        for i in indices:
            end_to_start[i+len(word)-1].append(i)

    compatible = [False] * (len(S)+1)

    compatible[0] = True
    for i in range(1, len(S)+1):
        compatible[i] = False
        for j in end_to_start[i-1]:
            if compatible[j]:
                compatible[i] = True
                break
    return compatible[len(S)]

import doctest
doctest.testmod()