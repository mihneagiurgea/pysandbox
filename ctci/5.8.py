def drawByte(byte, i=7, j=0):
    # Cut leading bytes [7..i+1]
    byte &= (1 << i) - 1
    # Cut trailing bytes [j-1..0]
    byte >>= j
    print bin(byte)[2:]

def draw(screen, width, x1, x2, y):
    for i in xrange(x1 / 8, x2 / 8 + 1):
        xfrom = i * 8
        xto = xfrom + 7
        xfrom = max(xfrom, x1)
        xto = min(xto, x2)
        drawByte(screen[i], 7 - xfrom % 8, 7 - xto % 8)
