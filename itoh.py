DIGITS = [
    'zero', 'one', 'two', 'three', 'four', 'five',
    'six', 'seven', 'eight', 'nine'
]
TEENS = [
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
    'sixteen', 'seventeen', 'eighteen', 'ninetween'
]

ITOH = {
    10: 'ten',
    20: 'twenty',
    30: 'thirty',
    40: 'fourty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety',
    100: 'hundred'
}

def itoh(n):
    """Integer to human."""
    pieces = []
    while n:
        if n >= 100:
            pieces.append(DIGITS[n / 100])
            pieces.append(ITOH[100])
            n %= 100
            if n:
                pieces.append('and')
        elif n >= 20:
            pieces.append(ITOH[n / 10 * 10])
            n %= 10
        elif n >= 10:
            pieces.append(TEENS[n - 10])
            n = 0
        else:
            pieces.append(DIGITS[n])
            n = 0
    return ' '.join(pieces)

for i in range(1, 1000):
    print '%d: %s' % (i, itoh(i))
