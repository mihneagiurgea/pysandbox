def is_match(s, p):
    """
    >>> is_match('a', 'aa')
    False
    >>> is_match('aa', 'aa')
    True
    >>> is_match('aaa', 'aa')
    False
    >>> is_match('zb', '.*')
    True
    >>> is_match('aab', 'c*a*b*')
    True
    >>> is_match('aabz', 'c*a*b*')
    False
    """
    if not s and not p:
        return True
    if s and not p:
        return False

    # From here on, len(p) > 0
    if len(p) == 1 or p[1] != '*':
        # Must match a single character.
        if p[0] == '.' or (s and s[0] == p[0]):
            return is_match(s[1:], p[1:])
        else:
            return False
    else:
        # Must match any sequence of characters (e.g.: 'a*' pattern).
        # Try to match exactly 0 characters.
        if is_match(s, p[2:]):
            return True
        # Try to match s[:i-1].
        for i in range(len(s)):
            if p[0] == '.' or s[i] == p[0]:
                if is_match(s[i+1:], p[2:]):
                    return True
            else:
                # s[i] does not match p[0], break
                break
        return False

if __name__ == '__main__':
    import doctest
    doctest.testmod()