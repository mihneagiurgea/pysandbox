def convert_to_bin(x, max_digits = 32):
    if not (0 <= x < 1):
        raise ValueError('invalid range')
    digits = []
    exp = 1.0
    while x != 0 and len(digits) <= max_digits:
        exp /= 2
        if x >= exp:
            digit = '1'
            x -= exp
        else:
            digit = '0'
        digits.append(digit)
    return '0.' + ''.join(digits)

def convert_to_bin2(x, max_digits = 32):
    if not (0 <= x < 1):
        raise ValueError('invalid range')
    digits = []
    while x != 0 and len(digits) <= max_digits:
        x *= 2
        if x >= 1:
            digit = '1'
            x -= 1
        else:
            digit = '0'
        digits.append(digit)
    return '0.' + ''.join(digits)

print convert_to_bin(0.5 + 0.125)
print convert_to_bin2(0.5 + 0.125)
