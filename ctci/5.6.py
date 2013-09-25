def swap_bits(x):
    mask = int('10' * 16, 2)
    return ((x << 1) & mask) | ((x & mask) >> 1)

for s in ['10101100', '1011100']:
    x = int(s, 2)
    sx = swap_bits(x)
    print 'x : %10s' % bin(x)
    print 'sx: %10s' % bin(sx)