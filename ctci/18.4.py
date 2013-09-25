def count2_up_to(n, digit=2):
    """

    >>> count2_up_to(1)
    0
    >>> count2_up_to(3)
    1
    >>> count2_up_to(13)
    2
    >>> count2_up_to(20)
    3
    >>> count2_up_to(23)
    7
    >>> count2_up_to(99)
    20
    >>> count2_up_to(101)
    20
    >>> count2_up_to(999)
    300
    >>> count2_up_to(9999)
    4000
    """
    count = 0
    base = 1
    while base <= n:
        count += n / (base * 10) * base
        x = n % (base * 10) - (digit * base - 1)
        if x > 0:
            count += min(x, base)
        base *= 10
    return count

if __name__ == '__main__':
    import doctest
    doctest.testmod()
