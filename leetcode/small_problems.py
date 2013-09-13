class LinkedList(object):

    def __init__(self, value, tail=None):
        self.value = value
        self.tail = tail

    def __repr__(self):
        if self.tail is None:
            return '%r-/->' % self.value
        else:
            return '%r-->%r' % (self.value, self.tail)

def count(root, key):
    sol = 0
    while root:
        if root.key == key:
            sol += root.left.size + 1
            break
        elif key < root.key:
            root = root.left
        else:
            sol += root.left.size + 1
            root = root.right
    return sol

def reverse(ll):
    last = None
    while ll is not None:
        tail = ll.tail
        ll.tail = last
        last = ll
        ll = tail
    return last

def swap_nodes_in_pair(ll):
    curr = ll
    last = pseudohead = LinkedList(-1, None)
    while curr is not None:
        if curr.tail is not None:
            next = curr.tail
            curr.tail = next.tail
            next.tail = curr
        else:
            next = curr
        last.tail = next
        last = curr
        curr = curr.tail
    return pseudohead.tail

def longest_valid_parentheses(s):
    # Best solution is [besti, bestj]
    besti = -1
    st = []
    D = [0] * len(s)
    for i, ch in enumerate(s):
        if ch == '(':
            st.append(i)
        elif st:
            j = st.pop()
            D[i] = i - j + 1 + D[j-1]
        if besti == -1 or D[i] > D[besti]:
            besti = i
    if besti == -1:
        return ''
    else:
        return s[besti - D[besti]+1:besti+1]

def main():
    s = ')))(()))((()((()())())'
    s = ')))((('
    print longest_valid_parentheses(s)

    # lls = []
    # lls.append(LinkedList(1))
    # for i in range(2, 6):
    #     node = LinkedList(i, lls[-1])
    #     lls.append(node)
    # ll = lls[2]
    # print '%r =>' % ll
    # print '%r' % reverse(ll)

def atoi(s):
    # Remove trailing and leading whitespaces
    s = s.strip()

    # Extract the sign
    sgn = +1
    if s[0] in '+-':
        sgn = +1 if s[0] == '+' else -1
        s = s[1:]

    if not s.isdigit():
        raise ValueError('Invalid s argument: %r' % s)

    return sgn * int(s)

ROMAN_SYMBOLS = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

def integer_to_roman(n):
    """
    Symbol to value:
    I   1
    V   5
    X   10
    L   50
    C   100
    D   500
    M   1000
    >>> integer_to_roman(1)
    'I'
    >>> integer_to_roman(3)
    'III'
    >>> integer_to_roman(4)
    'IV'
    >>> integer_to_roman(60)
    'LX'
    >>> integer_to_roman(91)
    'XCI'
    >>> integer_to_roman(239)
    'CCXXXIX'
    >>> integer_to_roman(3987)
    'MMMCMLXXXVII'
    """
    SYMBOLS = {
        1: ['I', 'V', 'X'],
        10: ['X', 'L', 'C'],
        100: ['C', 'D', 'M'],
        1000: ['M', None, None]
    }
    def convert_digit(symbols, digit):
        if 0 <= digit <= 3:
            return symbols[0] * digit
        elif digit == 4:
            return symbols[0] + symbols[1]
        elif 5 <= digit <= 8:
            return symbols[1] + symbols[0] * (digit - 5)
        elif digit == 9:
            return symbols[0] + symbols[2]

    result_digits = []
    base = 1
    while n:
        result_digits.append(convert_digit(SYMBOLS[base], n % 10))
        n /= 10
        base *= 10

    return ''.join(reversed(result_digits))

def roman_to_integer(roman):
    """

    >>> roman_to_integer(integer_to_roman(1)) == 1
    True
    >>> all(roman_to_integer(integer_to_roman(i)) == i for i in range(1, 10))
    True
    >>> all(roman_to_integer(integer_to_roman(i)) == i for i in range(10, 100))
    True
    >>> all(roman_to_integer(integer_to_roman(i)) == i for i in range(100, 4000))
    True
    """
    # Sum all digits up, then fix constructs of the form:
    # IX (instead of summing to 11, it actually represents 10 - 1 = 9).
    result = sum(ROMAN_SYMBOLS[c] for c in roman)
    for i in xrange(1, len(roman)):
        curr = ROMAN_SYMBOLS[roman[i]]
        prev = ROMAN_SYMBOLS[roman[i-1]]
        if curr > prev:
            result -= 2 * prev
    return result

def permutation_sequence(n, k):
    if n == 1:
        return [1]

    def fact(n):
        res = 1
        for i in range(2, n+1):
            res *= i
        return res
    x = fact(n-1)
    digit = (k - 1) / x + 1
    # k - (digit-1) * x =
    # = k - ( (k-1) / x + 1 - 1) * x
    # = k - ( (k-1) / x ) * x >= 1
    partial_permutation = permutation_sequence(n-1, k - (digit-1) * x)
    # partial_permutation uses digits from 1 to (n-1), but we've already
    # decided to use digit `digit` on the first position - bump other digits
    permutation = [digit]
    for d in partial_permutation:
        if d >= digit:
            d += 1
        permutation.append(d)
    return permutation

def next_combination(a, n, k):
    """
    >>> next_combination([1, 2, 3], 4, 3)
    [1, 2, 4]
    >>> next_combination([1, 2, 4], 4, 3)
    [1, 3, 4]
    >>> next_combination([2, 3, 4], 5, 3)
    [2, 3, 5]
    >>> next_combination([2, 3, 5], 5, 3)
    [2, 4, 5]
    >>> next_combination([2, 4, 5], 5, 3)
    [3, 4, 5]
    >>> next_combination([3, 4, 5], 5, 3) is None
    True
    """
    for i in range(k-1, -1, -1):
        # Can we increment this position?
        if a[i] + k - i <= n:
            a[i] += 1
            for j in range(i+1, k):
                a[j] = a[i] + j - i
            return a
    return None


def sort_three_colors(A):
    """
    >>> A = [2, 1, 0, 1, 0, 2, 1, 0, 1, 0, 1, 0]
    >>> sort_three_colors(A)
    >>> A == sorted(A)
    True
    >>> A = [2, 1, 0]
    >>> sort_three_colors(A)
    >>> A == sorted(A)
    True
    """
    def swap(i, j):
        A[i], A[j] = A[j], A[i]

    p = 0
    q = len(A)-1
    i = 0
    while i <= q:
        if A[i] == 0:
            swap(i, p)
            p += 1
            i += 1
        elif A[i] == 1:
            i += 1
        elif A[i] == 2:
            swap(i, q)
            q -= 1
        else:
            raise ValueError(A[i])

def subsets2(S):
    S.sort()

    def generate_all(S):
        if len(S) == 0:
            return [ [] ]
        x = S[0]
        count = S.count(x)
        subsets = []
        for subset in generate_all(S[count:]):
            for i in range(count+1):
                new_subset = [x] * i
                new_subset.extend(subset)
                subsets.append(new_subset)
        return subsets

    return generate_all(S)

if __name__ == '__main__':
    print subsets2([2, 1, 2])
    # print permutation_sequence(3, 5)
    # main()
    import doctest
    doctest.testmod()

